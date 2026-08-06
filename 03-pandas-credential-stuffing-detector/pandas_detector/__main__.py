from pathlib import Path
# Import the Pandas analysis functions.
from pandas_detector.detector import (
    build_five_minute_summary,
    count_attempts_by_ip,
    count_unique_users_by_ip,
    calculate_failure_metrics,
    detect_suspicious_windows
)
# Import the CSV loading function.
from pandas_detector.loader import load_authentication_logs
from pandas_detector.reporter import export_findings


def main() -> None:
    # Use the copied Task 02 attack dataset.
    log_file = Path("data/auth_attempts.csv")
    # Load the CSV into a Pandas DataFrame.
    logs = load_authentication_logs(log_file)
    # Build security measurements for each five-minute time window.
    five_minute_summary = build_five_minute_summary(logs)
    # Apply the credential-stuffing thresholds to the window summaries.
    suspicious_windows = detect_suspicious_windows(
    five_minute_summary
)
    # Define where the suspicious-window report will be saved.
    output_file = Path(
        "output/suspicious_windows.csv"
    )
    # Export the findings to CSV.
    saved_report = export_findings(
        suspicious_windows,
        output_file,
    )
    # Count authentication attempts for every source IP.
    attempt_counts = count_attempts_by_ip(logs)
    # Count distinct usernames attempted by every source IP.
    unique_user_counts = count_unique_users_by_ip(logs)
    # Calculate failed attempts and failure rates for every source IP.
    failure_metrics = calculate_failure_metrics(logs)
    # Display the grouped results.
    print("Authentication attempts by source IP")
    print("------------------------------------")
    print(attempt_counts)
    print()

    # Display the number of unique usernames for each source IP.
    print("Unique usernames by source IP")
    print("-----------------------------")
    print(unique_user_counts)
    print()

    # Display failure measurements for each source IP.
    print("Failure metrics by source IP")
    print("----------------------------")
    print(failure_metrics)
    print()

    # Display the five-minute summaries without Pandas row numbers.
    print("Five-minute authentication summary")
    print("----------------------------------")
    print(five_minute_summary.to_string(index=False))
    
    print()

    # Display only the time windows that matched both detection thresholds.
    print("Suspicious credential-stuffing windows")
    print("---------------------------------------")

    # Show a friendly message when no suspicious activity was found.
    if suspicious_windows.empty:
        print("No suspicious time windows detected.")
    else:
        print(
            suspicious_windows.to_string(
                index=False
            )
        )
    print()
    # Show where the CSV report was written.
    print(f"CSV report saved to: {saved_report.resolve()}")


if __name__ == "__main__":
    main()