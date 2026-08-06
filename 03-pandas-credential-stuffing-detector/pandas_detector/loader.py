from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {
    "timestamp",
    "username",
    "source_ip",
    "result",
}

def load_authentication_logs(file_path: Path) -> pd.DataFrame:
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Authentication log file not found: {file_path}"
        )
    
    logs = pd.read_csv(file_path)
    # validate that the required columns are present
    missing_columns = REQUIRED_COLUMNS.difference(logs.columns)

    if missing_columns:
        missing_names = ", ".join(sorted(missing_columns))

        raise ValueError(
            f"Missing required columns: {missing_names}"
        )

    try:
        logs["timestamp"] = pd.to_datetime(
            logs["timestamp"],
            errors="raise",
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Invalid timestamp found in authentication logs."
        ) from error

    return logs