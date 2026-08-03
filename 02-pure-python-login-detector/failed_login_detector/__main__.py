from pathlib import Path

from failed_login_detector.loader import load_attempts
from failed_login_detector.detector import (
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
        print(f"{source_ip}: {len(ip_attempts)} attempt(s)")


if __name__ == "__main__":
    main()