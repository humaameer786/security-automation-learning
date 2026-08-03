from pathlib import Path

from failed_login_detector.loader import load_attempts
from failed_login_detector.detector import (
    analyze_window,
    build_time_windows,
    group_attempts_by_ip,
    sort_attempts_by_time,
)

def main() -> None:
    # Load authentication attempts from a CSV file
    log_file = Path("data/auth_attempts.csv")
    attempts = load_attempts(log_file)
    # Group authentication attempts by source IP address
    attempts_by_ip = group_attempts_by_ip(attempts)
    # Sort authentication attempts by timestamp for each source IP
    attempts_by_ip = sort_attempts_by_time(attempts_by_ip)

    for source_ip, ip_attempts in attempts_by_ip.items():
        windows = build_time_windows(ip_attempts)
        largest_window = max(windows, key=len)
        analysis = analyze_window(largest_window)

        print(
            f"{source_ip}: "
            f"{analysis['total_attempts']} attempt(s), "
            f"{analysis['unique_users']} unique user(s), "
            f"{analysis['failed_attempts']} failure(s), "
            # Format the failure rate as a percentage with no decimal places
            f"{analysis['failure_rate']:.0%} failure rate"
        )


if __name__ == "__main__":
    main()