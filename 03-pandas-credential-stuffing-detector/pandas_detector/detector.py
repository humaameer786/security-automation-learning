import pandas as pd

def count_attempts_by_ip(logs: pd.DataFrame) -> pd.Series:
    # Group rows that have the same source_ip value.
    grouped_ips = logs.groupby("source_ip")
    # Count how many rows belong to each IP address.
    attempt_counts = grouped_ips.size()
    # Sort the results so the busiest IP appears first.
    attempt_counts = attempt_counts.sort_values(ascending=False)

    return attempt_counts