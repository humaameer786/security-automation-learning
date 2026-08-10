from security_event_store.database import (
    DATABASE_PATH,
    create_database,
)

# create the database and print the path
def main() -> None:
    create_database()

    print(
        f"Database ready: {DATABASE_PATH}"
    )

if __name__ == "__main__":
    main()