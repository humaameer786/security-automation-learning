from security_event_store.database import (
    DATABASE_PATH,
    create_database,
    insert_authentication_event,
)

# create the database and print the path
def main() -> None:
    create_database()

    event_id = insert_authentication_event(
        timestamp="2026-08-10 16:30:00",
        username="Patrick Jane",
        source_ip="203.0.113.10",
        source_system="vpn",
        event_type="login",
        result="success",
    )

    print(f"Stored authentication event with ID: {event_id}")
    print(f"Database: {DATABASE_PATH}")


if __name__ == "__main__":
    main()