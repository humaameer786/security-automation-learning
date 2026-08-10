# SQLite Security Event Store

A Python security automation project for storing and querying authentication events and security detections using SQLite.

## What the project does

The project uses SQLite as a persistent local database for security data.

It stores two types of records:

- authentication events
- security detections

Authentication events are inserted using parameterized SQL queries, while detections can be saved directly from Pandas DataFrames using `to_sql()`.

## Database tables

### authentication_events

Stores authentication activity such as:

- timestamp
- username
- source IP
- source system
- event type
- result

Example:

```text
Patrick Jane
203.0.113.10
vpn
login
success
```

### detections

Stores security alerts such as:

- timestamp
- username
- detection type
- severity
- description

Example:

```text
Baelor Targaryen
vpn_ip_mismatch
high
```

## Project structure

```text
05-sqlite-security-event-store/
├── data/
│   └── security_events.db
├── tests/
│   ├── __init__.py
│   └── test_database.py
├── security_event_store/
│   ├── __init__.py
│   ├── __main__.py
│   └── database.py
├── README.md
└── requirements.txt
```

## Setup

Create a Python 3.12 virtual environment:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the project

```powershell
python -m security_event_store
```

The application creates the SQLite database if it does not already exist and reads stored authentication events and detections.

## Database location

The SQLite database is created at:

```text
data/security_events.db
```

SQLite data remains stored after the Python program exits.

## Parameterized queries

Authentication events are inserted using SQL placeholders:

```sql
values (?, ?, ?, ?, ?, ?)
```

The values are supplied separately rather than being inserted directly into the SQL string.

This helps prevent SQL injection and avoids quoting problems.

## Pandas integration

Authentication events are read from SQLite using:

```python
pd.read_sql_query()
```

Detections are written from Pandas DataFrames using:

```python
DataFrame.to_sql()
```

## Run the tests

```powershell
python -m unittest discover -s tests -v
```

The tests verify:

- authentication events can be stored and read
- detections can be stored
- data persists between database connections
- temporary SQLite test databases are cleaned up correctly on Windows

## Technologies used

- Python 3.12
- SQLite
- Pandas
- unittest
- SQL

## Learning outcomes

This project demonstrates how to:

- create SQLite databases from Python
- design SQL tables
- use primary keys and autoincrement IDs
- insert data using parameterized queries
- read SQL data into Pandas
- save Pandas DataFrames using `to_sql()`
- persist security events between program runs
- manage SQLite connections safely
- write automated database tests
- use temporary databases during testing

## Security and privacy

All usernames, IP addresses, authentication events, and detections used in this project are synthetic.

No real credentials, production logs, API keys, or personal data are used.