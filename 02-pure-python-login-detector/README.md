# Pure-Python Failed-Login Detector

A beginner-friendly Python command-line tool that detects possible credential-stuffing activity in synthetic authentication logs.

This is Task 02 of the `security-automation-learning` repository. It builds the first simple version of the detection logic that will later be used in the final Security Automation Pipeline.

## What the detector looks for

An IP address is flagged when, within a rolling five-minute window, it has:

- At least five unique usernames
- A failure rate of at least 80%

This represents a possible credential-stuffing pattern: one source IP quickly trying several usernames, with most attempts failing.

## Features

- Uses only Python’s standard library
- Loads authentication attempts from CSV
- Converts timestamps into `datetime` objects
- Groups login attempts by source IP
- Sorts attempts chronologically
- Builds rolling five-minute windows
- Counts unique usernames and failed attempts
- Calculates failure rates
- Flags suspicious source IP addresses
- Accepts a CSV file path from the command line
- Includes automated tests
- Uses only synthetic logs and fictional IP addresses

## Project structure

```text
02-pure-python-login-detector/
├── failed_login_detector/
│   ├── __init__.py
│   ├── __main__.py
│   ├── detector.py
│   └── loader.py
├── data/
│   ├── auth_attempts.csv
│   ├── normal_attempts.csv
│   ├── malformed_attempts.csv
│   └── missing_columns.csv
├── tests/
│   ├── __init__.py
│   └── test_detector.py
└── README.md
```

## Requirements

- Python 3.12 or another supported Python 3 version
- Windows PowerShell

No external Python packages are required.

## Set up the virtual environment

From inside the Task 02 folder:

```powershell
# Create a virtual environment using Python 3.12.
py -3.12 -m venv .venv

# Activate the virtual environment in PowerShell.
.\.venv\Scripts\Activate.ps1
```

## Run the detector

Run the default attack sample:

```powershell
python -m failed_login_detector
```

Run the normal-traffic sample:

```powershell
python -m failed_login_detector .\data\normal_attempts.csv
```

View the command-line help:

```powershell
python -m failed_login_detector --help
```

## Test validation behaviour

Run the dataset containing malformed rows:

```powershell
python -m failed_login_detector .\data\malformed_attempts.csv
```

The invalid rows are skipped, while the valid credential-stuffing activity is still detected.

Run the file with a missing required CSV column:

```powershell
python -m failed_login_detector .\data\missing_columns.csv
```

Expected error:

```text
Error: could not load log file: Missing required CSV column(s): result
```

The detector validates:

- Required CSV headings
- Missing values
- Invalid timestamps
- Unsupported login results
- Unexpected extra CSV fields
- Missing files

## Expected suspicious finding

The attack sample should flag:

```text
Source IP:       203.0.113.50
Attempts:        6
Unique users:    6
Failed attempts: 5
Failure rate:    83%
```

The normal sample should report:

```text
No suspicious IP addresses detected.
```

## Run the automated tests

```powershell
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 4 tests in ...
OK
```

## CSV format

The detector expects:

```text
timestamp,username,source_ip,result
```

Example:

```csv
2026-08-02T10:10:00,charlie,203.0.113.50,failure
```

## Detection limitations

This is a learning project, not a production security system.

The thresholds are fixed and may create false positives or miss attacks in real traffic. A production detector would need configurable thresholds, stronger validation, larger datasets, and tuning based on real authentication behaviour.

## Security and privacy

All included authentication logs are synthetic.

The IP addresses use documentation-only ranges. Do not commit real authentication logs, passwords, API keys, `.env` files, or virtual environments.