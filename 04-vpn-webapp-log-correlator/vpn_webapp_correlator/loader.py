from pathlib import Path
import pandas as pd

# required columns for VPN and WebApp logs
VPN_REQUIRED_COLUMNS = {
    "timestamp",
    "username",
    "source_ip",
    "assigned_ip",
    "result",
}

WEBAPP_REQUIRED_COLUMNS = {
    "timestamp",
    "username",
    "source_ip",
    "action",
    "result",
}

# Load and validate VPN logs from a CSV file
def load_vpn_logs(file_path: Path) -> pd.DataFrame:
    if not file_path.is_file():
        raise FileNotFoundError(
            f"VPN log file not found: {file_path}"
        )

    logs = pd.read_csv(file_path)

    missing_columns = VPN_REQUIRED_COLUMNS.difference(
        logs.columns
    )

    if missing_columns:
        missing_names = ", ".join(
            sorted(missing_columns)
        )

        raise ValueError(
            f"VPN logs missing required columns: {missing_names}"
        )

    try:
        logs["timestamp"] = pd.to_datetime(
            logs["timestamp"],
            errors="raise",
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Invalid timestamp found in VPN logs."
        ) from error

    return logs

# Load and validate WebApp logs from a CSV file
def load_webapp_logs(file_path: Path) -> pd.DataFrame:
    if not file_path.is_file():
        raise FileNotFoundError(
            f"WebApp log file not found: {file_path}"
        )

    logs = pd.read_csv(file_path)

    missing_columns = WEBAPP_REQUIRED_COLUMNS.difference(
        logs.columns
    )

    if missing_columns:
        missing_names = ", ".join(
            sorted(missing_columns)
        )

        raise ValueError(
            f"WebApp logs missing required columns: {missing_names}"
        )

    try:
        logs["timestamp"] = pd.to_datetime(
            logs["timestamp"],
            errors="raise",
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Invalid timestamp found in WebApp logs."
        ) from error

    return logs