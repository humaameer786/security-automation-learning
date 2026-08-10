from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = PROJECT_ROOT / "data" / "security_events.db"

# create the database
def create_database(db_path: Path = DATABASE_PATH) -> None:
    db_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            create table if not exists authentication_events (
                id integer primary key autoincrement,
                timestamp text not null,
                username text not null,
                source_ip text not null,
                source_system text not null,
                event_type text not null,
                result text not null
            )
            """
        )
        
        connection.execute(
            """
            create table if not exists detections (
                id integer primary key autoincrement,
                timestamp text not null,
                username text not null,
                detection_type text not null,
                severity text not null,
                description text not null
            )
            """
        )
    
        connection.commit()

def insert_authentication_event(
    timestamp: str,
    username: str,
    source_ip: str,
    source_system: str,
    event_type: str,
    result: str,
    db_path: Path = DATABASE_PATH,
) -> int:
    # insert one authentication event into the database.

    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(
            """
            insert into authentication_events (
                timestamp,
                username,
                source_ip,
                source_system,
                event_type,
                result
            )
            values (?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                username,
                source_ip,
                source_system,
                event_type,
                result,
            ),
        )

        connection.commit()

        return cursor.lastrowid
    
# read authentication events from the database
def read_authentication_events(
    db_path: Path = DATABASE_PATH,
) -> pd.DataFrame:
    with sqlite3.connect(db_path) as connection:
        # runs this SQL query against the database and gives result as a Pandas DataFrame.
        events = pd.read_sql_query(
            """
            select
                id,
                timestamp,
                username,
                source_ip,
                source_system,
                event_type,
                result
            from authentication_events
            order by id
            """,
            connection,
        )

    return events

# save security detections to the database
def save_detections(
    detections: pd.DataFrame,
    db_path: Path = DATABASE_PATH,
) -> None:
    with sqlite3.connect(db_path) as connection:
        detections.to_sql(
            "detections",
            connection,
            if_exists="append",
            index=False,
        )