import tempfile
import unittest
from pathlib import Path

from pandas_detector.loader import load_authentication_logs


class TestAuthenticationLogLoader(unittest.TestCase):
    def test_missing_file_raises_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_folder:
            missing_file = Path(temporary_folder) / "missing.csv"

            with self.assertRaisesRegex(
                FileNotFoundError,
                "Authentication log file not found",
            ):
                load_authentication_logs(missing_file)

    def test_missing_required_column_raises_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_folder:
            log_file = Path(temporary_folder) / "missing_columns.csv"

            log_file.write_text(
                (
                    "timestamp,username,source_ip\n"
                    "2026-08-02 10:00:00,user1,192.0.2.10\n"
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "Missing required columns: result",
            ):
                load_authentication_logs(log_file)

    def test_invalid_timestamp_raises_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_folder:
            log_file = Path(temporary_folder) / "invalid_timestamp.csv"

            log_file.write_text(
                (
                    "timestamp,username,source_ip,result\n"
                    "not-a-timestamp,user1,192.0.2.10,failure\n"
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "Invalid timestamp found",
            ):
                load_authentication_logs(log_file)


if __name__ == "__main__":
    unittest.main()