import tempfile
import unittest
from pathlib import Path

import pandas as pd

from pandas_detector.detector import (
    build_five_minute_summary,
    detect_suspicious_windows,
)
from pandas_detector.loader import load_authentication_logs
from pandas_detector.reporter import export_findings


class TestFindingsReporter(unittest.TestCase):

    def test_findings_are_exported_to_csv(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        # load the synthetic attack dataset
        log_file = project_root / "data" / "auth_attempts.csv"
        logs = load_authentication_logs(log_file)
        # produce the suspicious finding that will be exported
        summary = build_five_minute_summary(logs)
        findings = detect_suspicious_windows(summary)
        # create a temporary folder so the test does not affect real output files
        with tempfile.TemporaryDirectory() as temporary_folder:
            output_file = (
                Path(temporary_folder)
                / "suspicious_windows.csv"
            )
            # export the findings to the temporary CSV file
            saved_file = export_findings(
                findings,
                output_file,
            )
            # confirm that the exporter returned the expected path
            self.assertEqual(saved_file, output_file)
            # confirm that the CSV file was created
            self.assertTrue(output_file.is_file())
            # load the exported file so its contents can be checked
            exported_findings = pd.read_csv(output_file)
            # confirm that exactly one suspicious window was exported
            self.assertEqual(len(exported_findings), 1)
            # confirm that the expected attacking IP was exported
            self.assertEqual(
                exported_findings.iloc[0]["source_ip"],
                "203.0.113.50",
            )


if __name__ == "__main__":
    # allow this test file to be run directly
    unittest.main()