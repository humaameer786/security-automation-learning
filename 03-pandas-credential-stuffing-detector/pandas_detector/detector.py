import pandas as pd

def count_attempts_by_ip(logs: pd.DataFrame) -> pd.Series:
    # Group rows that have the same source_ip value.
    grouped_ips = logs.groupby("source_ip")
    # Count how many rows belong to each IP address.
    attempt_counts = grouped_ips.size()
    # Sort the results so the busiest IP appears first.
    attempt_counts = attempt_counts.sort_values(ascending=False)

    return attempt_counts

def count_unique_users_by_ip(logs: pd.DataFrame) -> pd.Series:
    # Group rows by source IP, then select the username column.
    grouped_users = logs.groupby("source_ip")["username"]
    # nunique() counts distinct username values in each IP group.
    unique_user_counts = grouped_users.nunique()
    # Sort the busiest IPs first.
    unique_user_counts = unique_user_counts.sort_values(ascending=False)

    return unique_user_counts

def calculate_failure_metrics(logs: pd.DataFrame) -> pd.DataFrame:
    # Create a new Boolean column, true means the login result was "failure" and false means it wasnt.
    logs = logs.copy()
    logs["is_failure"] = logs["result"].eq("failure")
    # Group the authentication records by source IP.
    grouped_logs = logs.groupby("source_ip")
    # Build a summary table for each IP address.
    failure_metrics = grouped_logs.agg(
        # Count every authentication attempt in the group.
        total_attempts=("result", "size"),
        # Count True values in is_failure.
        # In Python, True behaves like 1 and False behaves like 0.
        failed_attempts=("is_failure", "sum"),
    )
    # Calculate the percentage of attempts that failed.
    failure_metrics["failure_rate"] = (
        failure_metrics["failed_attempts"]
        / failure_metrics["total_attempts"]
    )
    # Sort the IPs so the highest failure rate appears first.
    failure_metrics = failure_metrics.sort_values(
        by="failure_rate",
        ascending=False,
    )

    return failure_metrics