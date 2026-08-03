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


if __name__ == "__main__":
    unittest.main()