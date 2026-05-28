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

### Command Line Interface (Recommended)

The Hash Flagging System is primarily used via the command line. Here's how to run it with your data:

#### Basic Usage

```bash
# Analyze a CSV file and generate an HTML report
python main.py --file employees.csv --output report.html

# Analyze a JSON file with default settings
python main.py --file employees.json

# Analyze an Excel file
python main.py --file employee_data.xlsx --output report.html
```

#### Advanced Options

```bash
# Specify custom column names
python main.py --file data.csv \
    --id-column employee_id \
    --email-column email_address \
    --hash-column pwd_hash \
    --output report.html

# Set a higher threshold (only flag hashes appearing 3+ times)
python main.py --file employees.csv --threshold 3 --output report.json

# Export report in different formats
python main.py --file employees.json --output report.txt --output-format txt
python main.py --file employees.xml --output report.csv --output-format csv
python main.py --file employees.csv --output report.json --output-format json

# Enable case-sensitive hash comparison
python main.py --file employees.csv --case-sensitive --output report.html

# Verbose output for debugging
python main.py --file employees.csv --verbose --output report.html
```

#### Complete Example with Sample Data

If you have a CSV file (`employees.csv`) with the following structure:

```csv
id,email,password_hash
1,alice@example.com,5f4dcc3b5aa765d61d8327deb882cf99
2,bob@example.com,5f4dcc3b5aa765d61d8327deb882cf99
3,charlie@example.com,e99a18c428cb38ca5f28a972bf06f9ad
```

Run the command:

```bash
python main.py --file employees.csv --output report.html
```

This will:
1. Load all employee records from the CSV file
2. Detect duplicate password hashes (Alice and Bob share the same hash)
3. Generate a detailed HTML report showing:
   - Which employees share passwords
   - Risk levels (CRITICAL/HIGH/MEDIUM)
   - Recommendations for remediation

### Python API Usage

You can also use the system programmatically in your Python code:

```python
from core import HashFlagger
from loaders import FileLoader
from reporters import ReportGenerator

# Initialize the flagger
flagger = HashFlagger(case_sensitive=False)

# Load employee records (auto-detects format)
records = FileLoader.load('employees.csv')
flagger.add_records(records)

# Find duplicate hashes (threshold: 2 or more occurrences)
flagger.find_duplicates(threshold=2)

# Get results
summary = flagger.get_duplicate_summary()
flagged_employees = flagger.flag_employees()

# Print summary
print(f"Total Duplicate Hashes: {summary['total_duplicate_hashes']}")
print(f"Total Employees Affected: {summary['total_employees_affected']}")

# Generate and save report
reporter = ReportGenerator(flagged_employees, summary)
reporter.save_report('report.html', format_type='html')
```
## Supported Formats

The system automatically detects file formats based on file extension, or you can specify manually:

| Format | Extension | Description |
|--------|-----------|-------------|
| CSV | `.csv` | Comma-separated values |
| TSV | `.tsv` | Tab-separated values |
| JSON | `.json` | JSON arrays or objects |
| XML | `.xml` | XML formatted employee data |
| Excel | `.xlsx`, `.xls` | Microsoft Excel files |

## Command Line Options Reference

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--file` | `-f` | (required) | Path to employee records file |
| `--format` | | auto-detect | File format (csv, json, xml, xlsx, xls, tsv) |
| `--id-column` | | `id` | Name of the employee ID column |
| `--email-column` | | `email` | Name of the email column |
| `--hash-column` | | `password_hash` | Name of the password hash column |
| `--threshold` | | `2` | Minimum occurrences to flag as duplicate |
| `--output` | `-o` | (none) | Output file path for the report |
| `--output-format` | | `html` | Report format (html, json, csv, txt) |
| `--case-sensitive` | | false | Perform case-sensitive hash comparison |
| `--verbose` | `-v` | false | Enable verbose output |

## Configuration

Create a `config.yaml` file to customize default behavior:

```yaml
hash_algorithm: 'sha256'
case_sensitive: false
flag_threshold: 2  # Flag if hash appears 2 or more times
export_format: 'html'
```
## Report Output

The system generates detailed reports including:

- List of duplicate hashes with affected employees
- Security risk assessment
- Recommendations for remediation
- Export options (HTML, PDF, JSON, CSV)

## Security Considerations

- This tool processes sensitive data; store outputs securely
- Use HTTPS when transferring reports
- Consider encrypting the database of hashes
- Regular audits recommended

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please submit pull requests or issues.

## Support

For questions or issues, please open a GitHub issue.
