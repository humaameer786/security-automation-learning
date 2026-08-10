import unittest
from pathlib import Path

from vpn_webapp_correlator.correlator import (
    analyze_correlated_activity,
    correlate_by_username,
)
from vpn_webapp_correlator.loader import (
    load_vpn_logs,
    load_webapp_logs,
)
from vpn_webapp_correlator.normalizer import (
    normalize_vpn_logs,
    normalize_webapp_logs,
)

# test cases for the log correlation functions
class TestLogCorrelation(unittest.TestCase):
    def setUp(self) -> None:
        project_root = Path(__file__).resolve().parents[1]

        vpn_file = project_root / "data" / "vpn_logs.csv"
        webapp_file = project_root / "data" / "webapp_logs.csv"

        vpn_logs = load_vpn_logs(vpn_file)
        webapp_logs = load_webapp_logs(webapp_file)

        self.vpn_logs = normalize_vpn_logs(vpn_logs)
        self.webapp_logs = normalize_webapp_logs(webapp_logs)

    def test_logs_are_correlated_by_username(self) -> None:
        correlated = correlate_by_username(
            self.vpn_logs,
            self.webapp_logs,
        )

        self.assertEqual(len(correlated), 3)

        self.assertSetEqual(
            set(correlated["username"]),
            {
                "Patrick Jane",
                "Baelor Targaryen",
                "Elia Martell",
            },
        )

    def test_only_baelor_is_flagged(self) -> None:
        correlated = correlate_by_username(
            self.vpn_logs,
            self.webapp_logs,
        )

        analyzed = analyze_correlated_activity(
            correlated
        )

        suspicious = analyzed.loc[
            analyzed["is_suspicious"]
        ]

        self.assertEqual(len(suspicious), 1)

        self.assertEqual(
            suspicious.iloc[0]["username"],
            "Baelor Targaryen",
        )

    def test_baelor_has_expected_ip_mismatch(self) -> None:
        correlated = correlate_by_username(
            self.vpn_logs,
            self.webapp_logs,
        )

        analyzed = analyze_correlated_activity(
            correlated
        )

        baelor = analyzed.loc[
            analyzed["username"] == "Baelor Targaryen"
        ].iloc[0]

        self.assertEqual(
            baelor["vpn_assigned_ip"],
            "10.8.0.20",
        )

        self.assertEqual(
            baelor["webapp_source_ip"],
            "10.8.0.99",
        )

        self.assertFalse(baelor["ip_match"])

        self.assertEqual(
            baelor["time_difference_minutes"],
            1.0,
        )


if __name__ == "__main__":
    unittest.main()