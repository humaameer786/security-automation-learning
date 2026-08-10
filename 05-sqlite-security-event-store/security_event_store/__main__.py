import pandas as pd

from security_event_store.database import (
    DATABASE_PATH,
    create_database,
    read_authentication_events,
    save_detections,
)


def main() -> None:
    create_database()

    events = read_authentication_events()

    print("Stored authentication events:")
    print(events.to_string(index=False))

    detections = pd.DataFrame(
        [
            {
                "timestamp": "2026-08-10 16:35:00",
                "username": "Baelor Targaryen",
                "detection_type": "vpn_ip_mismatch",
                "severity": "high",
                "description": (
                    "WebApp source IP did not match "
                    "the VPN-assigned IP."
                ),
            }
        ]
    )

    save_detections(detections)

    print("\nStored 1 security detection.")
    print(f"\nDatabase: {DATABASE_PATH}")


if __name__ == "__main__":
    main()