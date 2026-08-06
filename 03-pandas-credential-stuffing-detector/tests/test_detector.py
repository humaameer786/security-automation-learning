import unittest
from pathlib import Path
from pandas_detector.detector import (
    build_five_minute_summary,
    detect_suspicious_windows,
)
from pandas_detector.loader import load_authentication_logs

class TestCredentialStuffingDetector(unittest.TestCase):
    def test_attack_dataset_produces_one_finding(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        # load the synthetic credential-stuffing dataset.
        log_file = project_root / "data" / "auth_attempts.csv"
        logs = load_authentication_logs(log_file)
        # build five-minute summaries and apply detection thresholds.
        summary = build_five_minute_summary(logs)
        findings = detect_suspicious_windows(summary)
        # confirm that exactly one suspicious window was detected.
        self.assertEqual(len(findings), 1)
        # select the detected row.
        finding = findings.iloc[0]
        # confirm that the expected attacking IP was detected.
        self.assertEqual(
            finding["source_ip"],
            "203.0.113.50",
        )
        # confirm the calculated security measurements.
        self.assertEqual(finding["total_attempts"], 6)
        self.assertEqual(finding["unique_users"], 6)
        self.assertEqual(finding["failed_attempts"], 5)
        # compare decimal values while allowing tiny rounding differences.
        self.assertAlmostEqual(
            finding["failure_rate"],
            5 / 6,
        )
    def test_normal_dataset_produces_no_findings(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        # load the synthetic normal traffic dataset
        log_file = project_root / "data" / "normal_attempts.csv"
        logs = load_authentication_logs(log_file)
        # summarize the activity and apply the detection thresholds
        summary = build_five_minute_summary(logs)
        findings = detect_suspicious_windows(summary)
        # confirm that normal activity does not produce an alert
        self.assertTrue(findings.empty)


if __name__ == "__main__":
    unittest.main()