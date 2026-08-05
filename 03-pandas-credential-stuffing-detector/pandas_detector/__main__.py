from pathlib import Path
# Import the Pandas analysis functions.
from pandas_detector.detector import (
    count_attempts_by_ip,
    count_unique_users_by_ip,
    calculate_failure_metrics,
)
# Import the CSV loading function.
from pandas_detector.loader import load_authentication_logs


def main() -> None:
    # Use the copied Task 02 attack dataset.
    log_file = Path("data/auth_attempts.csv")
    # Load the CSV into a Pandas DataFrame.
    logs = load_authentication_logs(log_file)
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


if __name__ == "__main__":
    main()