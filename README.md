# Fast SQL Injection Tester

A high-performance, asynchronous SQL injection vulnerability scanner designed for educational and authorized testing purposes. This tool helps security researchers and penetration testers identify potential SQL injection vulnerabilities in web applications with optimized performance and comprehensive reporting.

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/) [![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## 🔍 About

This project is a powerful SQL injection testing tool that helps security researchers and penetration testers identify potential SQL injection vulnerabilities in web applications. Built with performance in mind, it leverages asynchronous programming to perform rapid, efficient testing while maintaining a low resource footprint.

The tool is designed to be both powerful for professionals and accessible for learners, making it an excellent resource for:
- Security researchers conducting authorized testing
- Developers validating their application's security
- Students learning about web security
- DevSecOps teams integrating security testing into their pipelines

What sets this tool apart is its focus on performance, ease of use, and comprehensive reporting capabilities, all while maintaining ethical testing standards.

## ✨ Features

- 🚀 High-speed asynchronous testing
- 💪 Optimized payload detection
- 🌐 Support for both single URLs and bulk testing
- 📊 Real-time progress tracking
- 📝 JSON report generation
- 🔄 Connection pooling and DNS caching
- ⚡ Minimal resource usage

## 📥 Installation

### Option 1: Install globally (recommended) 🌍

```bash
# Clone the repository
git clone https://github.com/Zeeshan01001/sql-injection-tester-new.git
cd sql-injection-tester-new

# Install globally
pip install .

# Or install in development mode
pip install -e .
```

### Option 2: Run from source 💻

```bash
# Clone the repository
git clone https://github.com/Zeeshan01001/sql-injection-tester-new.git
cd sql-injection-tester-new

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Example Usage and Output

#### Testing a Secure Website

```console
$ sqli-tester -u "http://example.com"

✅ No vulnerabilities found
⠋ Testing parameters... [100%]
```

#### Testing a Vulnerable Website (Test Environment)

```console
$ sqli-tester -u "http://testphp.vulnweb.com/artists.php?artist=1"

🚨 [!] VULNERABILITIES FOUND [!] 🚨

Parameter: artist
Payload: " OR "1"="1
URL: http://testphp.vulnweb.com/artists.php?artist=%22+OR+%221%22%3D%221
Evidence: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
```

### Command Examples

#### Using global command (if installed globally) 🌐

```bash
# Test a single URL
sqli-tester -u "http://example.com/page.php?id=1"

# Test multiple URLs from a file
sqli-tester -f urls.txt

# Specify number of concurrent threads
sqli-tester -u "http://example.com/page.php?id=1" -t 30

# Save results to JSON file
sqli-tester -f urls.txt -o results.json
```

#### Running from source 💻

```bash
# Test a single URL
python3 sqli_tester.py -u "http://example.com/page.php?id=1"

# Test multiple URLs from a file
python3 sqli_tester.py -f urls.txt

# Specify number of concurrent threads
python3 sqli_tester.py -u "http://example.com/page.php?id=1" -t 30

# Save results to JSON file
python3 sqli_tester.py -f urls.txt -o results.json
```

### 🎮 Command Line Arguments

- `-u, --url`: Single URL to test
- `-f, --file`: File containing URLs to test (one per line)
- `-t, --threads`: Number of concurrent threads (default: 30)
- `-o, --output`: Output JSON file for results

## ⚠️ Disclaimer

This tool is for educational purposes and authorized testing only. Always obtain proper authorization before testing any website or application. Unauthorized testing may be illegal.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Check out our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with aiohttp for high-performance async operations
- Uses rich for beautiful console output 