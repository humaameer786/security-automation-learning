import csv
from datetime import datetime
from pathlib import Path

# Load authentication attempts from a CSV file
def load_attempts(file_path: Path) -> list[dict[str, object]]: 
    attempts = []

    with file_path.open(mode="r", encoding="utf-8", newline="") as log_file:
        reader = csv.DictReader(log_file)

        for row in reader:
            attempt = {
                # Convert the timestamp to a datetime object
                "timestamp": datetime.fromisoformat(row["timestamp"]),
                "username": row["username"].strip(),
                "source_ip": row["source_ip"].strip(),
                "result": row["result"].strip().lower(),
            }
            # Append the attempt to the list of attempts
            attempts.append(attempt)

    return attempts