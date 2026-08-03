from pathlib import Path

from failed_login_detector.loader import load_attempts
from failed_login_detector.detector import (
    detect_suspicious_ips,
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

    suspicious_ips = detect_suspicious_ips(attempts_by_ip)

    print("Suspicious IP Report")
    print("--------------------")

    if not suspicious_ips:
        print("No suspicious IP addresses detected.")
        return

    for finding in suspicious_ips:
        print(f"Source IP:       {finding['source_ip']}")
        print(
            f"Window:          {finding['window_start']} "
            f"to {finding['window_end']}"
        )
        print(f"Attempts:        {finding['total_attempts']}")
        print(f"Unique users:    {finding['unique_users']}")
        print(f"Failed attempts: {finding['failed_attempts']}")
        print(f"Failure rate:    {finding['failure_rate']:.0%}")


if __name__ == "__main__":
    main()