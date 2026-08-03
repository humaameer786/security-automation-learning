import csv
from datetime import datetime
# Path provides a clear and cross-platform way to work with file paths.
from pathlib import Path


# These are the columns every authentication log file must contain.
REQUIRED_COLUMNS = {
    "timestamp",
    "username",
    "source_ip",
    "result",
}

# These are the only login results accepted by this detector.
VALID_RESULTS = {
    "success",
    "failure",
}

def load_attempts(file_path: Path) -> list[dict[str, object]]:
    """Load valid authentication attempts from a CSV file."""

    # This list will contain every valid authentication attempt.
    attempts = []

    # Open the CSV safely.
    # The with statement automatically closes the file afterward.
    with file_path.open(
        mode="r",
        encoding="utf-8",
        newline="",
    ) as log_file:
        # DictReader uses the first row as column names.
        reader = csv.DictReader(log_file)

        # Check that the CSV contains all required column headings.
        actual_columns = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - actual_columns

        # A file with missing required columns cannot be processed reliably.
        if missing_columns:
            missing_list = ", ".join(sorted(missing_columns))

            raise ValueError(
                f"Missing required CSV column(s): {missing_list}"
            )

        # Start at line 2 because line 1 contains the CSV headings.
        for row_number, row in enumerate(reader, start=2):
            # DictReader stores unexpected extra values under the None key.
            if None in row:
                print(
                    f"Skipping line {row_number}: "
                    "unexpected extra field"
                )
                continue

            # Safely retrieve and clean each value.
            # The empty string prevents .strip() from failing on None.
            timestamp_text = (row.get("timestamp") or "").strip()
            username = (row.get("username") or "").strip()
            source_ip = (row.get("source_ip") or "").strip()
            result = (row.get("result") or "").strip().lower()

            # Reject rows where any required value is empty.
            if not timestamp_text or not username or not source_ip or not result:
                print(
                    f"Skipping line {row_number}: "
                    "missing required value"
                )
                continue

            # Convert the timestamp text into a datetime object.
            try:
                timestamp = datetime.fromisoformat(timestamp_text)
            except ValueError:
                print(
                    f"Skipping line {row_number}: "
                    "invalid timestamp"
                )
                continue

            # Reject login results other than success or failure.
            if result not in VALID_RESULTS:
                print(
                    f"Skipping line {row_number}: "
                    f"unsupported result '{result}'"
                )
                continue

            # Store the cleaned and validated authentication attempt.
            attempts.append(
                {
                    "timestamp": timestamp,
                    "username": username,
                    "source_ip": source_ip,
                    "result": result,
                }
            )

    # Return all valid records to the detector.
    return attempts