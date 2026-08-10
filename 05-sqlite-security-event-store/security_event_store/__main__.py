from security_event_store.database import (
    DATABASE_PATH,
    create_database,
    read_authentication_events,
    read_detections,
)


def main() -> None:
    create_database()

    events = read_authentication_events()
    detections = read_detections()

    print("Stored authentication events:")
    print(events.to_string(index=False))

    print("\nStored detections:")
    print(detections.to_string(index=False))

    print(f"\nDatabase: {DATABASE_PATH}")


if __name__ == "__main__":
    main()