from setuptools import setup, find_packages

setup(
    name="sqli-tester",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.9.0",
        "rich>=13.7.0",
        "typing-extensions>=4.8.0"
    ],
    entry_points={
        'console_scripts': [
            'sqli-tester=sqli_tester:main',
        ],
    },
    author="Zeeshan01001",
    description="A high-performance SQL injection vulnerability scanner",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Zeeshan01001/sql-injection-tester",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 