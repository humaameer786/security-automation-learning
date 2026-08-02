import csv
from datetime import datetime
from pathlib import Path


def read_logs(file_path: Path) -> dict[str, int] | None:
    valid_records = 0
    invalid_records = 0
    successful_logins = 0
    failed_logins = 0
    unique_users = set()
    unique_ips = set()

    with file_path.open(mode="r", encoding="utf-8", newline="") as log_file:
        # Use csv.DictReader to read the CSV file and map each row to a dictionary
        reader = csv.DictReader(log_file) 
        # Check if the required columns are present in the CSV file
        required_columns = {"timestamp", "username", "source_ip", "result"}
        actual_columns = set(reader.fieldnames or [])
        missing_columns = required_columns - actual_columns
        # If any required columns are missing, print a message and return
        if missing_columns:
            missing_list = ", ".join(sorted(missing_columns))
            print(f"Cannot parse log file: missing column(s): {missing_list}")
            return

        for row_number, row in enumerate(reader, start=2):
            # Skip invalid records
            if None in row:
                invalid_records += 1

                print(
                    f"Skipping invalid record on line {row_number}: "
                    "unexpected extra field"
                )
                continue
            timestamp_text = (row.get("timestamp") or "").strip()
            username = (row.get("username") or "").strip()
            source_ip = (row.get("source_ip") or "").strip()
            result = (row.get("result") or "").strip().lower()

            # Skip invalid records
            if not timestamp_text or not username or not source_ip or not result:
                invalid_records += 1

                print(
                    f"Skipping invalid record on line {row_number}: "
                    "missing required field"
                )
                continue

            try:
                # Convert the timestamp string to a datetime object
                timestamp = datetime.fromisoformat(timestamp_text)
            except ValueError:
                invalid_records += 1

                print(
                    f"Skipping invalid record on line {row_number}: "
                    "invalid timestamp"
                )
                continue
            
            if result not in {"success", "failure"}:
                invalid_records += 1

                print(
                    f"Skipping invalid record on line {row_number}: "
                    f"unsupported result '{result}'"
                )
                continue

            valid_records += 1
            unique_users.add(username)
            unique_ips.add(source_ip)

            if result == "success":
                successful_logins += 1
            elif result == "failure":
                failed_logins += 1

            print(
                f"{timestamp} | "
                f"{username} | "
                f"{source_ip} | "
                f"{result}"
            )

    return {
    "valid_records": valid_records,
    "successful_logins": successful_logins,
    "failed_logins": failed_logins,
    "unique_users": len(unique_users),
    "unique_ips": len(unique_ips),
    "invalid_records": invalid_records,
}