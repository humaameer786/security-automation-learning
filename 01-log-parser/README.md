# Authentication Log Parser

A beginner Python command-line project that reads synthetic authentication logs from a CSV file and prints a security summary.

This project is Task 01 of the `security-automation-learning` repository. It introduces Python virtual environments, packages, modules, CSV parsing, `datetime`, validation, and command-line arguments.

## Features

- Runs as a Python package using `python -m`
- Reads authentication records from CSV files
- Converts ISO-formatted timestamps into `datetime` objects
- Counts successful and failed login attempts
- Counts unique usernames and source IP addresses
- Detects malformed records without crashing
- Accepts an optional CSV file path
- Uses only synthetic logs and fictional documentation IP addresses

## Project structure

```text
01-log-parser/
├── auth_log_parser/
│   ├── __init__.py
│   ├── __main__.py
│   └── parser.py
├── data/
│   ├── auth_logs.csv
│   └── auth_logs_malformed.csv
└── README.md

## Requirements

- Python 3.12 or another supported Python 3 version
- Windows PowerShell

No external Python packages are required.

## Set up the virtual environment

From inside the `01-log-parser` folder:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Run the parser

Use the default clean sample file:

```powershell
python -m auth_log_parser
```

Use the malformed test file:

```powershell
python -m auth_log_parser .\data\auth_logs_malformed.csv
```

View command-line help:

```powershell
python -m auth_log_parser --help
```

## Expected clean-file summary

```text
Authentication Log Summary
--------------------------
Total valid records: 3
Successful logins:   1
Failed logins:       2
Unique users:        3
Unique IP addresses: 2
Invalid records:     0
```

## CSV format

The parser expects these columns:

```text
timestamp,username,source_ip,result
```

Supported login results are:

```text
success
failure
```

Result values are converted to lowercase, so values such as `SUCCESS` are also accepted.

## Security and privacy

All included logs are synthetic.

The sample IP addresses use documentation-only ranges. Do not commit real authentication logs, passwords, API keys, `.env` files, or virtual environments.