import argparse
from pathlib import Path

from pandas_detector.detector import (
    build_five_minute_summary,
    calculate_failure_metrics,
    count_attempts_by_ip,
    count_unique_users_by_ip,
    detect_suspicious_windows,
)
from pandas_detector.loader import load_authentication_logs
from pandas_detector.reporter import export_findings


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Detect possible credential-stuffing activity "
            "in authentication logs."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/auth_attempts.csv"),
        help="Path to the authentication log CSV file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/suspicious_windows.csv"),
        help="Path where the findings CSV will be saved.",
    )
    parser.add_argument(
        "--window-minutes",
        type=int,
        default=5,
        help="Size of each detection window in minutes.",
    )
    parser.add_argument(
        "--min-unique-users",
        type=int,
        default=5,
        help="Minimum number of unique usernames required.",
    )
    parser.add_argument(
        "--min-failure-rate",
        type=float,
        default=0.80,
        help="Minimum failed-login rate required.",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()

    logs = load_authentication_logs(arguments.input)

    attempt_counts = count_attempts_by_ip(logs)
    unique_user_counts = count_unique_users_by_ip(logs)
    failure_metrics = calculate_failure_metrics(logs)

    summary = build_five_minute_summary(
        logs,
        window_minutes=arguments.window_minutes,
    )

    findings = detect_suspicious_windows(
        summary,
        min_unique_users=arguments.min_unique_users,
        min_failure_rate=arguments.min_failure_rate,
    )

    saved_report = export_findings(
        findings,
        arguments.output,
    )

    print("Authentication attempts by source IP")
    print("------------------------------------")
    print(attempt_counts.to_string())

    print()
    print("Unique usernames by source IP")
    print("-----------------------------")
    print(unique_user_counts.to_string())

    print()
    print("Failure metrics by source IP")
    print("----------------------------")
    print(failure_metrics.to_string())

    print()
    print("Suspicious credential-stuffing windows")
    print("---------------------------------------")

    if findings.empty:
        print("No suspicious time windows detected.")
    else:
        print(findings.to_string(index=False))

    print()
    print(f"CSV report saved to: {saved_report.resolve()}")


if __name__ == "__main__":
    main()