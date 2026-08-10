import pandas as pd

## normalize VPN and WebApp logs by stripping whitespace, converting to lowercase, and renaming columns
def normalize_vpn_logs(logs: pd.DataFrame) -> pd.DataFrame:
    normalized = logs.copy() # working on a copy to avoid modifying the original DataFrame

    normalized["username"] = normalized["username"].str.strip()
    normalized["result"] = normalized["result"].str.strip().str.lower()

    normalized = normalized.rename(
        columns={
            "timestamp": "vpn_timestamp",
            "source_ip": "vpn_source_ip",
            "assigned_ip": "vpn_assigned_ip",
            "result": "vpn_result",
        }
    )

    return normalized

def normalize_webapp_logs(logs: pd.DataFrame) -> pd.DataFrame:
    normalized = logs.copy()

    normalized["username"] = normalized["username"].str.strip()
    normalized["action"] = normalized["action"].str.strip().str.lower()
    normalized["result"] = normalized["result"].str.strip().str.lower()

    normalized = normalized.rename(
        columns={
            "timestamp": "webapp_timestamp",
            "source_ip": "webapp_source_ip",
            "action": "webapp_action",
            "result": "webapp_result",
        }
    )

    return normalized