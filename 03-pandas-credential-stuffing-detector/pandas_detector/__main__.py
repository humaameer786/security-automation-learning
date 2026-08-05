from pathlib import Path
from pandas_detector.loader import load_authentication_logs
from pandas_detector.detector import count_attempts_by_ip


def main() -> None:
    # Use the copied Task 02 attack dataset.
    log_file = Path("data/auth_attempts.csv")
    # Load the CSV into a Pandas DataFrame.
    logs = load_authentication_logs(log_file)
    # Count authentication attempts for every source IP.
    attempt_counts = count_attempts_by_ip(logs)
    # Display the grouped results.
    print("Authentication attempts by source IP")
    print("------------------------------------")
    print(attempt_counts)


if __name__ == "__main__":
    main()