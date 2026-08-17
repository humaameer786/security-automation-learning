import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from threat_intel_enricher.cache import cache_report, get_cached_report

from threat_intel_enricher.client import VirusTotalAPIError, get_ip_report

from threat_intel_enricher.parser import parse_ip_report
from threat_intel_enricher.validator import validate_ip

# test IP address validation
class TestValidator(unittest.TestCase):
    def test_valid_ip(self):
        self.assertEqual(
            validate_ip("8.8.8.8"),
            "8.8.8.8",
        )

    def test_invalid_ip(self):
        with self.assertRaises(ValueError):
            validate_ip("999.999.999.999")
# test parsing useful fields from VirusTotal reports
class TestParser(unittest.TestCase):
    # mock dict
    def test_parse_report(self):
        report = {
            "data": {
                "id": "8.8.8.8",
                "attributes": {
                    "country": "US",
                    "asn": 15169,
                    "as_owner": "Google LLC",
                    "reputation": 100,
                    "last_analysis_stats": {
                        "malicious": 1,
                        "suspicious": 0,
                        "harmless": 50,
                        "undetected": 40,
                    },
                },
            }
        }

        result = parse_ip_report(report)

        self.assertEqual(
            result["ip_address"],
            "8.8.8.8",
        )
        self.assertEqual(
            result["malicious"],
            1,
        )
# test saving and loading cached reports
class TestCache(unittest.TestCase):
    def test_cache_report(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir)/"cache.json"
            
            with patch(
                "threat_intel_enricher.cache.CACHE_PATH",
                cache_path
            ):
                report = {
                    "data": {
                        "id": "8.8.8.8"
                    }
                }

                cache_report(
                    "8.8.8.8",
                    report
                )

                cached_report = get_cached_report("8.8.8.8")

                self.assertEqual(
                    cached_report,
                    report
                )
# test VirusTotal API error handling
class TestClient(unittest.TestCase):
    @patch("threat_intel_enricher.client.requests.get")
    def test_unauthorized_api_key(
        self,
        mock_get
    ):
        response = Mock()
        response.status_code = 401
        mock_get.return_value = response

        with self.assertRaises(VirusTotalAPIError):
            get_ip_report(
                "8.8.8.8",
                "fake_key"
            )

    @patch("threat_intel_enricher.client.requests.get")
    def test_timeout(
        self,
        mock_get
    ):
        mock_get.side_effect = requests.Timeout()

        with self.assertRaises(VirusTotalAPIError):
            get_ip_report(
                "8.8.8.8",
                "fake_key"
            )

if __name__ == "__main__":
    unittest.main()