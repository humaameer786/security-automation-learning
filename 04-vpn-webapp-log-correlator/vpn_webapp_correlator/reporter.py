from pathlib import Path
import pandas as pd

# a report containing only suspicious correlated activity.
def build_suspicious_alerts(
    analyzed_logs: pd.DataFrame,
) -> pd.DataFrame:

    alerts = analyzed_logs.loc[
        analyzed_logs["is_suspicious"]
    ].copy()

    alerts["reason"] = (
        "WebApp login occurred within the time window, "
        "but the source IP did not match the VPN-assigned IP."
    )

    alerts = alerts[
        [
            "username",
            "vpn_timestamp",
            "vpn_source_ip",
            "vpn_assigned_ip",
            "webapp_timestamp",
            "webapp_source_ip",
            "time_difference_minutes",
            "reason",
        ]
    ]

    return alerts.reset_index(drop=True)

# export the suspicious alerts to a CSV file
def export_alerts(
    alerts: pd.DataFrame,
    output_file: Path,
) -> Path:

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    alerts.to_csv(
        output_file,
        index=False,
    )

    return output_file