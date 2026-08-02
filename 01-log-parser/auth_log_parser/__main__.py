from pathlib import Path
import argparse

from auth_log_parser.parser import read_logs

def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read authentication logs and print a summary."
    )

    parser.add_argument(
        "log_file",
        nargs="?",
        type=Path,
        default=Path("data/auth_logs.csv"),
        help="Path to the authentication log CSV file.",
    )

    return parser

def main() -> None:
    # Create the argument parser and parse the command-line arguments
    arguments = create_argument_parser().parse_args()
    log_file = arguments.log_file
    if not log_file.is_file():
        print(f"Error: log file not found: {log_file}")
        return
    summary = read_logs(log_file)

    if summary is None:
        return

    print()
    print("Authentication Log Summary")
    print("--------------------------")
    print(f"Total valid records: {summary['valid_records']}")
    print(f"Successful logins:   {summary['successful_logins']}")
    print(f"Failed logins:       {summary['failed_logins']}")
    print(f"Unique users:        {summary['unique_users']}")
    print(f"Unique IP addresses: {summary['unique_ips']}")
    print(f"Invalid records:     {summary['invalid_records']}")


if __name__ == "__main__":
    main()