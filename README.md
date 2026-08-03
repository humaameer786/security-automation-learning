# Security Automation Learning Journey

This repository documents my step-by-step learning journey toward building a complete **Security Automation Pipeline**.

Instead of beginning with one large project that contains several unfamiliar technologies, I am building each component separately. This allows me to understand the logic, test each part independently, document what I learn, and eventually combine the components into a complete cybersecurity portfolio project.

> **Status:** In progress  
> **Primary language:** Python  
> **Focus:** Security automation, log analysis, threat detection, APIs, databases, and Docker

---

## Project Goal

The goal of this repository is to develop the practical skills required to automate common security-analysis tasks.

The exercises will cover:

- Parsing authentication logs
- Working with timestamps and time windows
- Detecting failed-login patterns
- Detecting credential-stuffing attacks
- Correlating events from multiple log sources
- Using Pandas for security-data analysis
- Storing events in SQLite and PostgreSQL
- Enriching suspicious IP addresses through threat-intelligence APIs
- Managing API keys and other secrets safely
- Containerizing applications with Docker
- Running multiple services with Docker Compose
- Testing, debugging, and documenting security tools

---

## Planned Learning Path

### 01 — Security Log Parser

Build a Python command-line tool that reads authentication logs and displays:

- Total valid records
- Successful logins
- Failed logins
- Unique usernames
- Unique source IP addresses
- Invalid or malformed records

Concepts:

- Python virtual environments
- Python modules
- Running code with `python -m`
- CSV processing
- `datetime` parsing
- Input validation
- Error handling

**Status:** Done

---

### 02 — Pure-Python Failed-Login Detector

Create a detector using Python dictionaries, lists, sets, and time-window logic.

Planned detection rule:

> Flag a source IP when it attempts multiple usernames within a short time period and most attempts fail.

Concepts:

- Dictionaries and sets
- Sorting events by timestamp
- `datetime` and `timedelta`
- Grouping events by source IP
- Threshold-based detection
- Basic unit testing

**Status:** In progress

---

### 03 — Pandas Credential-Stuffing Detector

Rebuild the detection logic using Pandas.

Concepts:

- DataFrames
- `pandas.to_datetime()`
- Boolean filtering
- `groupby()`
- `nunique()`
- `resample()`
- Aggregation
- Exporting detections to CSV

The Pandas detector will be compared with the pure-Python version to confirm that both produce the same results.

**Status:** Not started

---

### 04 — VPN and Web Application Log Correlator

Create synthetic VPN authentication logs and web-application access logs, then correlate related activity across both sources.

The tool will investigate:

- Whether the same IP targeted both systems
- Whether the same usernames appeared in both logs
- Whether repeated failures were followed by a successful login
- Whether events occurred within the same time window

Concepts:

- Log normalization
- Multi-source analysis
- Pandas `merge()`
- Timestamp comparison
- Event correlation

**Status:** Not started

---

### 05 — SQLite Security Event Store

Store authentication events and detection results in SQLite.

Planned workflow:

```text
Synthetic authentication logs
              ↓
        SQLite database
              ↓
         Pandas analysis
              ↓
          Detections
              ↓
        SQLite database
```

Concepts:

- Creating databases and tables
- Parameterized SQL queries
- Inserting records from Python
- `pandas.read_sql()`
- DataFrame `to_sql()`
- Querying suspicious activity
- Data persistence

**Status:** Not started

---

### 06 — Threat Intelligence IP Enricher

Build a command-line tool that checks suspicious IP addresses using a threat-intelligence API.

Planned features:

- Validate IPv4 and IPv6 addresses
- Read an API key from an environment variable
- Send authenticated API requests
- Parse JSON responses
- Display useful reputation information
- Handle timeouts and API errors
- Respect API rate limits
- Cache previously checked IP addresses

Error handling will include:

- Missing API key
- Invalid IP address
- Network timeout
- HTTP `401`
- HTTP `404`
- HTTP `429`
- Unexpected API responses

**Status:** Not started

---

### 07 — PostgreSQL and JSONB

Store threat-intelligence enrichment results in PostgreSQL.

Concepts:

- Connecting Python to PostgreSQL
- Database connection strings
- SQLAlchemy or `psycopg2`
- Transactions
- PostgreSQL `JSONB`
- Storing raw API responses
- Querying previous enrichment results
- Duplicate handling and upserts

**Status:** Not started

---

### 08 — Dockerized Security Tool

Package one Python security tool inside a Docker container.

Concepts:

- Docker images and containers
- Dockerfiles
- Base images
- Image layers
- Environment variables
- Volume mounts
- `.dockerignore`
- Running containers as a non-root user

**Status:** Not started

---

### 09 — Docker Compose Application and Database

Run the Python application and PostgreSQL as separate services using Docker Compose.

Planned architecture:

```text
Python security application
             ↓
   PostgreSQL database
```

Concepts:

- Multi-container applications
- Docker Compose services
- Container networking
- Persistent volumes
- Environment-variable injection
- Database health checks
- Service startup order
- Container logs and restart testing

**Status:** Not started

---

## Final Portfolio Project

After completing the learning exercises, I will combine the components into a separate project:

# Security Automation Pipeline

The final pipeline will:

1. Generate synthetic VPN and web-application authentication logs.
2. Store and process security events.
3. Detect credential-stuffing patterns.
4. Correlate suspicious activity across multiple log sources.
5. Enrich suspicious IP addresses using a threat-intelligence API.
6. Store enrichment results in PostgreSQL.
7. Run the complete workflow through one Python orchestrator.
8. Package the application and database using Docker Compose.

The completed pipeline will be published as its own GitHub repository.

---

## Documentation Approach

Each exercise will include its own README covering:

- Objective
- Concepts practised
- Detection logic
- Setup instructions
- Usage
- Example input
- Example output
- What I learned
- Problems encountered and fixes
- Limitations
- Possible future improvements

This repository is intended to show both the final results and the learning process behind them.

---

## Security and Privacy

All logs and security events used in this repository will be:

- Synthetic
- Fictional
- Created specifically for learning
- Free from real credentials
- Free from personal information
- Free from confidential business data

Reserved documentation IP ranges will be used where appropriate:

```text
192.0.2.0/24
198.51.100.0/24
203.0.113.0/24
```

This repository does not involve unauthorized access, real credential collection, or testing external systems without permission.

---

## Secrets Management

API keys, passwords, tokens, and database credentials will never be committed to GitHub.

The repository’s `.gitignore` should include:

```gitignore
.env
.venv/
venv/
__pycache__/
*.pyc
*.db
.pytest_cache/
.vscode/
.idea/
```

A safe example file may be included:

```text
.env.example
```

Example:

```env
VT_API_KEY=replace_with_your_api_key
DATABASE_URL=replace_with_your_database_connection
```

---

## Current Progress

| Stage | Exercise | Status |
|---:|---|---|
| 01 | Security Log Parser | In progress |
| 02 | Pure-Python Failed-Login Detector | Not started |
| 03 | Pandas Credential-Stuffing Detector | Not started |
| 04 | VPN and WebApp Log Correlator | Not started |
| 05 | SQLite Security Event Store | Not started |
| 06 | Threat Intelligence IP Enricher | Not started |
| 07 | PostgreSQL and JSONB | Not started |
| 08 | Dockerized Security Tool | Not started |
| 09 | Docker Compose Application and Database | Not started |

This table will be updated as the project progresses.

---

## Skills Being Developed

- Python
- Security automation
- Authentication-log analysis
- Credential-stuffing detection
- Event correlation
- Pandas
- SQL
- SQLite
- PostgreSQL
- JSON and JSONB
- REST APIs
- Threat intelligence
- Secrets management
- Docker
- Docker Compose
- Git and GitHub
- Testing and debugging
- Technical documentation

---

## Disclaimer

This repository contains defensive cybersecurity exercises performed with synthetic data and controlled environments.

It is intended solely for legal and educational use. The tools and techniques documented here should not be used to access, test, monitor, or interfere with systems without the system owner’s explicit authorization.

---

## Author

**Huma Ameer**

