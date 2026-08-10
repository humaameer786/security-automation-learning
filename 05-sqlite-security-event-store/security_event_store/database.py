from pathlib import Path
import sqlite3

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