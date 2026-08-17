# Threat Intelligence IP Enricher

A Python command-line security automation tool that validates IP addresses, queries the VirusTotal API for threat-intelligence data, extracts useful security information, handles common API and network errors, and caches previous results locally to avoid unnecessary API requests.

This project is part of my hands-on cybersecurity automation learning roadmap.

---

## Features

- Validates IPv4 and IPv6 addresses before performing a lookup
- Loads the VirusTotal API key securely from a `.env` file
- Sends authenticated requests to the VirusTotal API v3
- Extracts useful threat-intelligence fields from the JSON response
- Displays:
  - IP address
  - country
  - ASN
  - AS owner
  - VirusTotal reputation
  - malicious detections
  - suspicious detections
  - harmless detections
  - undetected results
- Handles:
  - invalid IP addresses
  - invalid or rejected API keys
  - missing VirusTotal reports
  - API rate limits
  - request timeouts
  - other HTTP and network errors
- Caches VirusTotal responses locally
- Reuses cached results instead of making repeated API requests
- Includes automated tests using Python's built-in `unittest`
- Uses mocks so API-related tests do not consume real VirusTotal requests

---

## Project Structure

```text
06-threat-intelligence-ip-enricher/
│
├── data/
│   └── cache.json
│
├── tests/
│   ├── __init__.py
│   └── test_threat_intel_enricher.py
│
├── threat_intel_enricher/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cache.py
│   ├── client.py
│   ├── config.py
│   ├── parser.py
│   └── validator.py
│
├── .env
├── .env.example
├── README.md
└── requirements.txt
```

### Main Components

| File | Purpose |
|---|---|
| `validator.py` | Validates IPv4 and IPv6 addresses |
| `config.py` | Loads the VirusTotal API key from `.env` |
| `client.py` | Sends requests to the VirusTotal API and handles API/network errors |
| `parser.py` | Extracts useful threat-intelligence fields from VirusTotal responses |
| `cache.py` | Saves and retrieves previous API responses |
| `__main__.py` | Connects all components and provides the command-line interface |
| `test_threat_intel_enricher.py` | Contains automated tests for the main functionality |

---

## Requirements

- Python 3.12+
- VirusTotal API key
- Internet connection for uncached lookups

Python dependencies are listed in `requirements.txt`.

```text
requests==2.34.2
python-dotenv==1.2.2
```

---

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/humaameer786/security-automation-learning.git
```

Move into the project directory:

```powershell
cd security-automation-learning\06-threat-intelligence-ip-enricher
```

---

### 2. Create a virtual environment

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, temporarily allow local scripts for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## VirusTotal API Key

Create a VirusTotal account and obtain an API key.

The project reads the key from a local `.env` file.

The included `.env.example` shows the required format:

```env
VT_API_KEY=replace_with_your_api_key
```

Create your own `.env` file in the project root:

```env
VT_API_KEY=your_real_virustotal_api_key
```

The `.env` file must never be committed to GitHub.

Do not place a real API key inside `.env.example`.

---

## Usage

Run the tool from the project root:

```powershell
python -m threat_intel_enricher
```

Enter an IP address when prompted:

```text
Enter an IP address: 8.8.8.8
```

For a new IP address, the tool queries VirusTotal:

```text
Source: VirusTotal API

Threat intelligence report
--------------------------
IP address: 8.8.8.8
Country: US
ASN: 15169
AS owner: Google LLC
Reputation: 556
Malicious detections: 1
Suspicious detections: 0
Harmless detections: 52
Undetected: 38
```

VirusTotal results can change over time, so detection counts and reputation values may be different when the same IP is checked later.

---

## Local Caching

After a successful VirusTotal lookup, the complete API response is stored in:

```text
data/cache.json
```

If the same IP address is checked again, the tool uses the stored result:

```text
Enter an IP address: 8.8.8.8
Source: local cache
```

This avoids making unnecessary VirusTotal API requests.

The basic flow is:

```text
IP address entered
        |
        v
validate IP
        |
        v
check local cache
     /       \
   found    not found
     |          |
     v          v
use cache   query VirusTotal
                |
                v
            save result
                |
                v
           parse report
                |
                v
          display output
```

---

## Error Handling

The tool converts common failures into readable messages instead of displaying large Python tracebacks.

### Invalid IP address

```text
Enter an IP address: 999.999.999.999
Invalid IP address: 999.999.999.999
```

### Rejected API key

```text
VirusTotal rejected the API key.
```

### Report not found

```text
No VirusTotal report was found for this IP.
```

### Rate limit reached

```text
VirusTotal API rate limit reached.
```

### Request timeout

```text
VirusTotal request timed out.
```

### Connection failure

```text
Could not connect to VirusTotal.
```

Other HTTP failures are also converted into readable error messages containing the returned HTTP status code.

---

## Automated Tests

The project uses Python's built-in `unittest` framework.

Run all tests with:

```powershell
python -m unittest discover -s tests -v
```

Current test coverage includes:

- valid IP validation
- invalid IP rejection
- VirusTotal response parsing
- saving and retrieving cached reports
- rejected API key handling
- request timeout handling

Example successful test run:

```text
test_cache_report (test_threat_intel_enricher.TestCache.test_cache_report) ... ok
test_timeout (test_threat_intel_enricher.TestClient.test_timeout) ... ok
test_unauthorized_api_key (test_threat_intel_enricher.TestClient.test_unauthorized_api_key) ... ok
test_parse_report (test_threat_intel_enricher.TestParser.test_parse_report) ... ok
test_invalid_ip (test_threat_intel_enricher.TestValidator.test_invalid_ip) ... ok
test_valid_ip (test_threat_intel_enricher.TestValidator.test_valid_ip) ... ok

----------------------------------------------------------------------
Ran 6 tests

OK
```

The API tests use mocked HTTP requests.

This means:

- no real API key is required for those tests
- no real VirusTotal request is sent
- no VirusTotal API quota is consumed

The cache test also uses a temporary cache file instead of modifying the real `data/cache.json`.

---

## Security Considerations

This project intentionally keeps secrets separate from source code.

### API keys

The VirusTotal API key is:

- stored in `.env`
- loaded at runtime with `python-dotenv`
- never hardcoded in Python files
- never printed to the terminal
- never included in `.env.example`

### Git

The real `.env` file should remain ignored by Git.

Before pushing changes, always make sure `.env` does not appear in GitHub Desktop's changed files.

### Cached Data

`data/cache.json` may contain:

- IP addresses that were investigated
- VirusTotal enrichment data
- network ownership information
- reputation and detection results

For this learning project, public test IP addresses such as `8.8.8.8` are suitable.

Do not commit investigation data containing sensitive or private operational information to a public repository.

---

## What I Practiced

This project helped me practice several concepts used in security automation and blue-team tooling:

- Python modules and project structure
- IPv4 and IPv6 validation
- REST API requests
- API authentication using headers
- environment variables
- secret management with `.env`
- JSON parsing
- dictionaries and nested API data
- exception handling
- HTTP status-code handling
- network timeout handling
- local JSON caching
- file handling with `pathlib`
- automated testing
- mocking external API requests
- separating validation, API, parsing, caching, and configuration logic

---

## Example Workflow

```text
Analyst enters IP
       |
       v
IP validation
       |
       v
Check cache
       |
       +--------------------+
       |                    |
   cache hit            cache miss
       |                    |
       v                    v
cached report        VirusTotal API
                            |
                            v
                       cache report
                            |
       +--------------------+
       |
       v
parse useful fields
       |
       v
display threat intelligence
```

---

## Possible Future Improvements

The current version focuses on the core threat-intelligence enrichment workflow.

Possible future improvements include:

- command-line arguments instead of interactive input
- batch enrichment of multiple IP addresses
- CSV or JSON output
- cache expiration
- timestamps for cached results
- risk scoring
- support for additional threat-intelligence providers
- enrichment of domains, URLs, and file hashes
- more automated tests
- structured logging

These are outside the current project scope but could be added in a future version.

---

## Disclaimer

This project is built for cybersecurity education and defensive security automation.

VirusTotal data should be treated as one source of threat intelligence rather than definitive proof that an IP address is malicious or safe. Detection results can change over time and should be interpreted together with other security evidence.