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