import argparse

# Path gives us a safer and clearer way to work with file paths.
from pathlib import Path

# Import the detection functions we created in detector.py.
from failed_login_detector.detector import (
    detect_suspicious_ips,
    group_attempts_by_ip,
    sort_attempts_by_time,
)

# Import the function that reads authentication attempts from a CSV file.
from failed_login_detector.loader import load_attempts

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and return the command-line argument parser."""

    # Create the command-line parser and describe what the program does.
    parser = argparse.ArgumentParser(
        description="Detect credential-stuffing patterns in authentication logs."
    )

    # Add an optional positional argument for the CSV file path.
    #
    # nargs="?" means the user may provide zero or one file path.
    # type=Path converts the text path into a Path object.
    # default is used when the user does not provide a file path.
    parser.add_argument(
        "log_file",
        nargs="?",
        type=Path,
        default=Path("data/auth_attempts.csv"),
        help="Path to the authentication log CSV file.",
    )

    return parser

def main() -> None:
    """Run the failed-login detector."""

    # Read the command-line arguments supplied by the user.
    arguments = create_argument_parser().parse_args()

    # Get the CSV file path from the parsed arguments.
    log_file = arguments.log_file

    # Stop safely if the supplied file does not exist.
    if not log_file.is_file():
        print(f"Error: log file not found: {log_file}")
        return

    # Read the authentication attempts from the CSV file.
    attempts = load_attempts(log_file)

    # Group all attempts by their source IP address.
    attempts_by_ip = group_attempts_by_ip(attempts)

    # Sort each IP address's attempts from earliest to latest.
    attempts_by_ip = sort_attempts_by_time(attempts_by_ip)

    # Apply the credential-stuffing detection rules.
    suspicious_ips = detect_suspicious_ips(attempts_by_ip)

    # Print the report heading.
    print("Suspicious IP Report")
    print("--------------------")

    # Show a friendly message when no suspicious IPs were found.
    if not suspicious_ips:
        print("No suspicious IP addresses detected.")
        return

    # Display the details for every suspicious IP address.
    for finding in suspicious_ips:
        print(f"Source IP:       {finding['source_ip']}")

        # Display the start and end time of the suspicious activity window.
        print(
            f"Window:          {finding['window_start']} "
            f"to {finding['window_end']}"
        )

        # Display the measurements used by the detection rule.
        print(f"Attempts:        {finding['total_attempts']}")
        print(f"Unique users:    {finding['unique_users']}")
        print(f"Failed attempts: {finding['failed_attempts']}")

        # :.0% converts a decimal such as 0.83 into 83%.
        print(f"Failure rate:    {finding['failure_rate']:.0%}")

if __name__ == "__main__":
    main()