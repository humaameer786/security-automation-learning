from pathlib import Path
from pandas_detector.detector import (
    build_five_minute_summary,
    count_attempts_by_ip,
    count_unique_users_by_ip,
    calculate_failure_metrics,
    detect_suspicious_windows
)
from pandas_detector.loader import load_authentication_logs
from pandas_detector.reporter import export_findings


def main() -> None:
    log_file = Path("data/auth_attempts.csv")
    logs = load_authentication_logs(log_file)
    # build security measurements for each five-minute time window.
    five_minute_summary = build_five_minute_summary(logs)
    # apply the credential-stuffing thresholds to the window summaries.
    suspicious_windows = detect_suspicious_windows(
    five_minute_summary
)
    # define where the suspicious-window report will be saved.
    output_file = Path(
        "output/suspicious_windows.csv"
    )
    saved_report = export_findings(
        suspicious_windows,
        output_file,
    )
    # count authentication attempts for every source IP.
    attempt_counts = count_attempts_by_ip(logs)
    # count distinct usernames attempted by every source IP.
    unique_user_counts = count_unique_users_by_ip(logs)
    # calculate failed attempts and failure rates for every source IP.
    failure_metrics = calculate_failure_metrics(logs)
    # display the grouped results.
    print("Authentication attempts by source IP")
    print("------------------------------------")
    print(attempt_counts)
    print()

    # display the number of unique usernames for each source IP.
    print("Unique usernames by source IP")
    print("-----------------------------")
    print(unique_user_counts)
    print()

    # display failure measurements for each source IP.
    print("Failure metrics by source IP")
    print("----------------------------")
    print(failure_metrics)
    print()

    # display the five-minute summaries without Pandas row numbers.
    print("Five-minute authentication summary")
    print("----------------------------------")
    print(five_minute_summary.to_string(index=False))
    
    print()

    # display only the time windows that matched both detection thresholds.
    print("Suspicious credential-stuffing windows")
    print("---------------------------------------")

    if suspicious_windows.empty:
        print("No suspicious time windows detected.")
    else:
        print(
            suspicious_windows.to_string(
                index=False
            )
        )
    print()
    print(f"CSV report saved to: {saved_report.resolve()}")


if __name__ == "__main__":
    main()