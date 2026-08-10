import pandas as pd

# match VPN and WebApp records belonging to the same user
def correlate_by_username(
    vpn_logs: pd.DataFrame,
    webapp_logs: pd.DataFrame,
) -> pd.DataFrame:

    correlated = pd.merge(
        vpn_logs,
        webapp_logs,
        on="username",
        how="inner",
    )

    return correlated

# analyze the correlated activity to identify suspicious behavior
def analyze_correlated_activity(
    correlated_logs: pd.DataFrame,
    max_minutes: int = 5,
) -> pd.DataFrame:

    analyzed = correlated_logs.copy()

    analyzed["time_difference_minutes"] = (
        analyzed["webapp_timestamp"]
        - analyzed["vpn_timestamp"]
    ).dt.total_seconds() / 60

    analyzed["ip_match"] = (
        analyzed["vpn_assigned_ip"]
        == analyzed["webapp_source_ip"]
    )

    analyzed["within_time_window"] = (
        analyzed["time_difference_minutes"]
        .between(0, max_minutes)
    )

    # flag activity when the webapp login happens soon after the vpn login
    # but comes from a different IP than the one assigned by the vpn
    analyzed["is_suspicious"] = (
        analyzed["within_time_window"]
        & ~analyzed["ip_match"]
        & analyzed["vpn_result"].eq("success")
        & analyzed["webapp_result"].eq("success")
        & analyzed["webapp_action"].eq("login")
    )

    return analyzed