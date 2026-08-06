import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


class TestCommandLineInterface(unittest.TestCase):
    def test_custom_input_and_output_options(self) -> None:
        """The CLI should accept custom paths and create a findings report."""

        project_root = Path(__file__).resolve().parents[1]
        input_file = project_root / "data" / "auth_attempts.csv"

        with tempfile.TemporaryDirectory() as temporary_folder:
            output_file = (
                Path(temporary_folder)
                / "custom_findings.csv"
            )

            command = [
                sys.executable,
                "-m",
                "pandas_detector",
                "--input",
                str(input_file),
                "--output",
                str(output_file),
                "--window-minutes",
                "5",
                "--min-unique-users",
                "5",
                "--min-failure-rate",
                "0.80",
            ]

            # run the detector with the same python environment as the tests
            result = subprocess.run(
                command,
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=result.stderr,
            )

            self.assertTrue(output_file.is_file())

            exported_findings = pd.read_csv(output_file)

            self.assertEqual(len(exported_findings), 1)
            self.assertEqual(
                exported_findings.iloc[0]["source_ip"],
                "203.0.113.50",
            )


if __name__ == "__main__":
    unittest.main()