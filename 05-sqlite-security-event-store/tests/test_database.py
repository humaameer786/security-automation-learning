import tempfile
import unittest
from pathlib import Path
import sqlite3

from contextlib import closing

import pandas as pd

from security_event_store.database import (
    create_database,
    insert_authentication_event,
    read_authentication_events,
    save_detections,
)

# test sqlite security event storage.
class TestSecurityEventStore(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.db_path = (
            Path(self.temporary_directory.name)
            / "security_events.db"
        )

        create_database(self.db_path)

    # test that authentication events can be stored and retrieved from the database
    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_authentication_event_can_be_stored(self) -> None:
        event_id = insert_authentication_event(
            timestamp="2026-08-10 16:30:00",
            username="Patrick Jane",
            source_ip="203.0.113.10",
            source_system="vpn",
            event_type="login",
            result="success",
            db_path=self.db_path,
        )

        self.assertEqual(event_id, 1)

        events = read_authentication_events(
            self.db_path
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events.iloc[0]["username"],
            "Patrick Jane",
        )

    def test_detection_can_be_stored(self) -> None:
        detections = pd.DataFrame(
            [
                {
                    "timestamp": "2026-08-10 16:35:00",
                    "username": "Baelor Targaryen",
                    "detection_type": "vpn_ip_mismatch",
                    "severity": "high",
                    "description": "Synthetic test detection.",
                }
            ]
        )

        save_detections(
            detections,
            self.db_path,
        )


        with closing(sqlite3.connect(self.db_path)) as connection:
            stored = pd.read_sql_query(
                "SELECT * FROM detections;",
                connection,
            )

        self.assertEqual(len(stored), 1)
        self.assertEqual(
            stored.iloc[0]["username"],
            "Baelor Targaryen",
        )

    def test_data_persists_between_connections(self) -> None:
        insert_authentication_event(
            timestamp="2026-08-10 17:00:00",
            username="Elia Martell",
            source_ip="192.0.2.30",
            source_system="webapp",
            event_type="login",
            result="success",
            db_path=self.db_path,
        )

        events = read_authentication_events(
            self.db_path
        )

        self.assertEqual(len(events), 1)
        self.assertEqual(
            events.iloc[0]["username"],
            "Elia Martell",
        )


if __name__ == "__main__":
    unittest.main()