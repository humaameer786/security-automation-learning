from pathlib import Path

from auth_log_parser.parser import read_logs


def main() -> None:
    log_file = Path("data/auth_logs.csv")
    read_logs(log_file)


if __name__ == "__main__":
    main()