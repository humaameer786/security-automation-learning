# VPN and WebApp Log Correlator

A Python security automation project that correlates synthetic VPN and web-application logs to identify suspicious activity across multiple systems.

## What the project does

The project reads two separate log sources:

- VPN authentication logs
- WebApp authentication logs

It normalizes their fields, matches activity belonging to the same user, compares timestamps and IP addresses, and generates a combined alert when suspicious cross-system activity is detected.

## Detection rule

A correlated event is considered suspicious when:

- the VPN authentication succeeded
- the WebApp login succeeded
- the WebApp login happened within 5 minutes of the VPN login
- the WebApp source IP does not match the IP assigned by the VPN

## Example detection

The synthetic dataset contains one suspicious user:

```text
Baelor Targaryen
```

VPN activity:

```text
VPN timestamp:   2026-08-08 10:05:00
VPN source IP:   198.51.100.20
VPN assigned IP: 10.8.0.20
```

WebApp activity:

```text
WebApp timestamp: 2026-08-08 10:06:00
WebApp source IP: 10.8.0.99
```

The events happened one minute apart, but the WebApp source IP does not match the VPN-assigned IP.

Patrick Jane and Elia Martell represent normal activity.

## Project structure

```text
04-vpn-webapp-log-correlator/
├── data/
│   ├── vpn_logs.csv
│   └── webapp_logs.csv
├── output/
│   └── correlated_alerts.csv
├── tests/
│   ├── __init__.py
│   ├── test_correlator.py
│   └── test_loader.py
├── vpn_webapp_correlator/
│   ├── __init__.py
│   ├── __main__.py
│   ├── correlator.py
│   ├── loader.py
│   ├── normalizer.py
│   └── reporter.py
├── README.md
└── requirements.txt
```

## VPN log format

The VPN CSV contains:

```text
timestamp
username
source_ip
assigned_ip
result
```

## WebApp log format

The WebApp CSV contains:

```text
timestamp
username
source_ip
action
result
```

## Normalization

The two log sources use similar column names for different meanings.

The normalizer renames them into clearer fields such as:

```text
vpn_timestamp
vpn_source_ip
vpn_assigned_ip
vpn_result

webapp_timestamp
webapp_source_ip
webapp_action
webapp_result
```

The `username` field is kept consistent so the two datasets can be correlated.

## Correlation

Pandas `merge()` is used to match VPN and WebApp records belonging to the same username.

The correlator then calculates:

```text
time_difference_minutes
ip_match
within_time_window
is_suspicious
```

## Setup

Create the virtual environment using Python 3.12:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the project

From the Task 04 folder:

```powershell
python -m vpn_webapp_correlator
```

The program should detect one suspicious correlated event for Baelor Targaryen.

## Run the tests

```powershell
python -m unittest discover -s tests -v
```

All tests should pass.

## Output

Suspicious correlated events are exported to:

```text
output/correlated_alerts.csv
```

The report combines evidence from both the VPN and WebApp logs.

## Validation

The log loader checks for:

- missing files
- missing required columns
- invalid timestamps

This prevents malformed input data from silently reaching the correlation logic.

## Technologies used

- Python 3.12
- Pandas
- unittest
- CSV
- virtual environments

## Learning outcomes

This project demonstrates how to:

- work with multiple security log sources
- normalize different log formats
- correlate events using shared fields
- merge Pandas DataFrames
- compare timestamps
- calculate time differences
- compare network addresses
- create cross-system detection rules
- validate input logs
- write automated tests
- export combined security alerts

## Security and privacy

All authentication events, usernames, and IP addresses used in this project are synthetic.

No real credentials, passwords, API keys, production logs, or personal data are used.