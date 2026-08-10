from pathlib import Path
from vpn_webapp_correlator.loader import (
    load_vpn_logs,
    load_webapp_logs,
)

from vpn_webapp_correlator.normalizer import (
    normalize_vpn_logs,
    normalize_webapp_logs,
)

from vpn_webapp_correlator.correlator import (
    analyze_correlated_activity,
    correlate_by_username,
)

from vpn_webapp_correlator.reporter import (
    build_suspicious_alerts,
    export_alerts,
)

# print the loaded logs to the console
def main() -> None:
    vpn_file = Path("data/vpn_logs.csv")
    webapp_file = Path("data/webapp_logs.csv")

    vpn_logs = load_vpn_logs(vpn_file)
    webapp_logs = load_webapp_logs(webapp_file)
    
    vpn_logs = normalize_vpn_logs(vpn_logs)
    webapp_logs = normalize_webapp_logs(webapp_logs)
    
    correlated_logs = correlate_by_username(
        vpn_logs,
        webapp_logs,
    )
    
    analyzed_logs = analyze_correlated_activity(
        correlated_logs
    )
    
    alerts = build_suspicious_alerts(
        analyzed_logs
    )

    output_file = Path(
        "output/correlated_alerts.csv"
    )

    saved_report = export_alerts(
        alerts,
        output_file,
    )

    print("VPN logs")
    print("--------")
    print(vpn_logs.to_string(index=False))

    print()
    print("WebApp logs")
    print("-----------")
    print(webapp_logs.to_string(index=False))
    
    print()
    print("Correlated VPN and WebApp activity")
    print("----------------------------------")
    print(correlated_logs.to_string(index=False))
    
    print()
    print("Correlation analysis")
    print("--------------------")
    print(
        analyzed_logs[
            [
                "username",
                "time_difference_minutes",
                "vpn_assigned_ip",
                "webapp_source_ip",
                "ip_match",
                "within_time_window",
                "is_suspicious",
            ]
        ].to_string(index=False)
    )
    
    print()
    print("Suspicious cross-system alerts")
    print("------------------------------")

    if alerts.empty:
        print("No suspicious correlated activity detected.")
    else:
        print(alerts.to_string(index=False))

    print()
    print(f"Alert report saved to: {saved_report.resolve()}")


if __name__ == "__main__":
    main()
    
