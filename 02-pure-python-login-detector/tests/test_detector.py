import unittest
from pathlib import Path

from failed_login_detector.detector import (
    detect_suspicious_ips,
    group_attempts_by_ip,
    sort_attempts_by_time,
)
from failed_login_detector.loader import load_attempts


# Get the parent directory of the current file
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load authentication attempts from a CSV file, group them by source IP, sort them by timestamp, and detect suspicious IP addresses
def detect_from_file(file_name: str) -> list[dict[str, object]]:
    file_path = PROJECT_ROOT / "data" / file_name
    attempts = load_attempts(file_path)
    attempts_by_ip = group_attempts_by_ip(attempts)
    attempts_by_ip = sort_attempts_by_time(attempts_by_ip)

    return detect_suspicious_ips(attempts_by_ip)

# Test the detect_from_file function
class FailedLoginDetectorTests(unittest.TestCase):
    def test_attack_sample_flags_expected_ip(self) -> None:
        findings = detect_from_file("auth_attempts.csv")

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["source_ip"], "203.0.113.50")
        self.assertEqual(findings[0]["unique_users"], 6)
        self.assertEqual(findings[0]["failed_attempts"], 5)
        self.assertAlmostEqual(findings[0]["failure_rate"], 5 / 6)

    def test_normal_sample_creates_no_alerts(self) -> None:
        findings = detect_from_file("normal_attempts.csv")

        self.assertEqual(findings, [])
        
    def test_malformed_rows_are_skipped_safely(self) -> None:
    # Load and analyze the dataset containing both valid and invalid rows.
        findings = detect_from_file("malformed_attempts.csv")

        # The valid attack records should still produce exactly one finding.
        self.assertEqual(len(findings), 1)

        # Confirm that the correct synthetic IP address was detected.
        self.assertEqual(
            findings[0]["source_ip"],
            "203.0.113.50",
        )

        # Only the six valid attack attempts should reach the detector.
        self.assertEqual(findings[0]["total_attempts"], 6)
        self.assertEqual(findings[0]["unique_users"], 6)
        self.assertEqual(findings[0]["failed_attempts"], 5)
    
    def test_missing_required_columns_raise_clear_error(self) -> None:
    # Build the full path to the deliberately broken CSV file.
        file_path = PROJECT_ROOT / "data" / "missing_columns.csv"

        # Confirm the loader raises the expected clear validation error.
        with self.assertRaisesRegex(
            ValueError,
            r"Missing required CSV column\(s\): result",
        ):
            load_attempts(file_path)


if __name__ == "__main__":
    unittest.main()