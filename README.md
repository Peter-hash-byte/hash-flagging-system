# Hash Flagging System

A comprehensive security tool for detecting duplicate password hashes across employee records. This system helps identify potential security vulnerabilities where employees may be sharing passwords or using the same credentials.

## Features

- **Multi-Format Support**: Handle CSV, JSON, XML, Excel, and database formats
- **Duplicate Detection**: Identify matching password hashes across employee records
- **Security Analysis**: Flag suspicious patterns and potential vulnerabilities
- **Detailed Reporting**: Generate comprehensive reports with flagged duplicates
- **Performance Optimized**: Efficient hash comparison for large datasets

## Installation

```bash
git clone https://github.com/peter-hash-byte/hash-flagging-system.git
cd hash-flagging-system
pip install -r requirements.txt
```

## Usage
### Basic Usage
```bash
from hash_flagging_system import HashFlagger

# Initialize the flagger
flagger = HashFlagger()

# Load employee records (auto-detects format)
flagger.load_records('employees.csv')

# Find duplicate hashes
duplicates = flagger.find_duplicates()

# Generate report
report = flagger.generate_report()
print(report)

```
## Command Line Usage
```bash
python main.py --file employees.json --output report.html
python main.py --file employees.csv --format csv --threshold 2
```
## Supported Formats

    CSV - Comma-separated values
    JSON - JSON arrays or objects
    XML - XML formatted employee data
    Excel - .xlsx and .xls files
    SQL - Database connections
    TSV - Tab-separated values
