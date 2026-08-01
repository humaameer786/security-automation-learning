import csv
from datetime import datetime
from pathlib import Path


def read_logs(file_path: Path) -> None: 
    valid_records = 0
    invalid_records = 0

    with file_path.open(mode="r", encoding="utf-8", newline="") as log_file:
        reader = csv.DictReader(log_file)

        for row_number, row in enumerate(reader, start=2):
            try:
                timestamp = datetime.fromisoformat(row["timestamp"])
            except ValueError:
                invalid_records += 1

                print(
                    f"Skipping invalid record on line {row_number}: "
                    "invalid timestamp"
                )
                continue

            valid_records += 1

            print(
                f"{timestamp} | "
                f"{row['username']} | "
                f"{row['source_ip']} | "
                f"{row['result']}"
            )

    print()
    print(f"Valid records:   {valid_records}")
    print(f"Invalid records: {invalid_records}")