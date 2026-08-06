# Pandas Credential-Stuffing Detector

A Python security automation project that uses Pandas to analyze authentication logs and identify possible credential-stuffing activity.

The detector groups login attempts by source IP and fixed time windows. It flags a window when:

- at least 5 different usernames were attempted
- at least 80% of the login attempts failed

The project uses synthetic authentication data only.

## Features

- loads authentication logs from CSV files
- validates required columns and timestamps
- groups activity into configurable time windows
- calculates login attempts, unique users, failures, and failure rates
- detects suspicious credential-stuffing windows
- exports findings to CSV
- supports configurable command-line options
- includes automated tests

## Project structure

```text
03-pandas-credential-stuffing-detector/
├── data/
│   ├── auth_attempts.csv
│   └── normal_attempts.csv
├── notebooks/
│   └── understanding_pandas.ipynb
├── pandas_detector/
│   ├── __init__.py
│   ├── __main__.py
│   ├── detector.py
│   ├── loader.py
│   └── reporter.py
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_detector.py
│   ├── test_loader.py
│   └── test_reporter.py
├── README.md
└── requirements.txt

The output folder is created automatically when a report is exported.

## CSV format

The input CSV file must contain these columns:

```text
timestamp,username,source_ip,result
```

Example:

```csv
timestamp,username,source_ip,result
2026-08-02 10:10:00,user1,203.0.113.50,failure
```

## Setup

From the Task 03 folder, create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required dependency:

```powershell
python -m pip install -r requirements.txt
```

## Run the detector

Run the detector using the default dataset and settings:

```powershell
python -m pandas_detector
```

The default settings are:

```text
input file: data/auth_attempts.csv
output file: output/suspicious_windows.csv
window size: 5 minutes
minimum unique users: 5
minimum failure rate: 0.80
```

## Command-line options

Display the available command-line options:

```powershell
python -m pandas_detector --help
```

Run the detector using custom options:

```powershell
python -m pandas_detector `
    --input .\data\auth_attempts.csv `
    --output .\output\custom_findings.csv `
    --window-minutes 5 `
    --min-unique-users 5 `
    --min-failure-rate 0.80
```

## Run the tests

Run all automated tests from the Task 03 folder:

```powershell
python -m unittest discover -s tests -v
```

All tests should pass.

## Expected detection

The synthetic attack dataset should detect this source IP:

```text
203.0.113.50
```

Its five-minute window contains:

```text
6 authentication attempts
6 unique usernames
5 failed attempts
83.33% failure rate
```

The normal authentication dataset should produce no suspicious findings.

## Output

Detected suspicious windows are exported to:

```text
output/suspicious_windows.csv
```

The output folder is created automatically when the detector runs.

The generated CSV report contains:

```text
source_ip
window_start
window_end
total_attempts
unique_users
failed_attempts
failure_rate
```

## Detection logic

A time window is considered suspicious when both of these conditions are met:

- at least five unique usernames were attempted
- at least 80% of the authentication attempts failed

Using both conditions helps avoid treating a single failed login as credential-stuffing activity.

## Technologies used

- Python
- Pandas
- argparse
- unittest
- CSV
- virtual environments

## Learning outcomes

This project demonstrates how to:

- load CSV security logs into a Pandas DataFrame
- convert timestamp strings into datetime values
- group authentication activity by source IP
- count unique usernames with `nunique()`
- calculate failed-login rates
- resample events into fixed time windows
- filter suspicious activity using multiple conditions
- validate CSV structure and timestamps
- export findings to CSV
- create configurable command-line tools
- test detection logic with automated tests

## Security and privacy

All IP addresses and authentication records used in this project are synthetic.

The project does not contain:

- real credentials
- real usernames
- passwords
- API keys
- production logs
- personal data
