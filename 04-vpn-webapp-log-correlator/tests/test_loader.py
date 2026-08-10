import tempfile
import unittest
from pathlib import Path

from vpn_webapp_correlator.loader import (
    load_vpn_logs,
    load_webapp_logs,
)

# test cases for the log loader functions
class TestLogLoader(unittest.TestCase):
    def test_missing_vpn_file_raises_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_folder:
            missing_file = Path(temporary_folder) / "vpn.csv"

            with self.assertRaisesRegex(
                FileNotFoundError,
                "VPN log file not found",
            ):
                load_vpn_logs(missing_file)

    def test_vpn_missing_required_column_raises_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_folder:
            log_file = Path(temporary_folder) / "vpn.csv"

            log_file.write_text(
                (
                    "timestamp,username,source_ip,result\n"
                    "2026-08-08 10:00:00,Patrick Jane,"
                    "203.0.113.10,success\n"
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "VPN logs missing required columns: assigned_ip",
            ):
                load_vpn_logs(log_file)

    def test_webapp_missing_required_column_raises_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_folder:
            log_file = Path(temporary_folder) / "webapp.csv"

            log_file.write_text(
                (
                    "timestamp,username,source_ip,result\n"
                    "2026-08-08 10:02:00,Patrick Jane,"
                    "10.8.0.10,success\n"
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "WebApp logs missing required columns: action",
            ):
                load_webapp_logs(log_file)

    def test_invalid_webapp_timestamp_raises_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_folder:
            log_file = Path(temporary_folder) / "webapp.csv"

            log_file.write_text(
                (
                    "timestamp,username,source_ip,action,result\n"
                    "not-a-date,Patrick Jane,"
                    "10.8.0.10,login,success\n"
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "Invalid timestamp found in WebApp logs",
            ):
                load_webapp_logs(log_file)


if __name__ == "__main__":
    unittest.main()