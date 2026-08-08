from pathlib import Path
import pandas as pd

# load vpn and webapp logs from csv files and convert timestamp to datetime object
def load_vpn_logs(file_path: Path) -> pd.DataFrame:
    logs = pd.read_csv(file_path)

    logs["timestamp"] = pd.to_datetime(
        logs["timestamp"],
        errors="raise",
    )

    return logs

def load_webapp_logs(file_path: Path) -> pd.DataFrame:
    logs = pd.read_csv(file_path)

    logs["timestamp"] = pd.to_datetime(
        logs["timestamp"],
        errors="raise",
    )

    return logs