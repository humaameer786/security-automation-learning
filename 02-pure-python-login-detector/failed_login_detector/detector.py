from datetime import datetime

def group_attempts_by_ip(
    attempts: list[dict[str, object]],
) -> dict[str, list[dict[str, object]]]:
    attempts_by_ip = {}

    for attempt in attempts:
        source_ip = str(attempt["source_ip"])

        if source_ip not in attempts_by_ip:
            attempts_by_ip[source_ip] = []

        attempts_by_ip[source_ip].append(attempt)

    return attempts_by_ip

def get_attempt_timestamp(attempt: dict[str, object]) -> datetime:
    timestamp = attempt["timestamp"]

    if not isinstance(timestamp, datetime):
        raise TypeError("Authentication attempt timestamp must be a datetime.")

    return timestamp

# Sort authentication attempts by timestamp for each source IP
def sort_attempts_by_time(
    attempts_by_ip: dict[str, list[dict[str, object]]],
) -> dict[str, list[dict[str, object]]]:
    sorted_attempts_by_ip = {}

    for source_ip, ip_attempts in attempts_by_ip.items():
        # Sort the attempts for this source IP by timestamp
        sorted_attempts_by_ip[source_ip] = sorted(
            ip_attempts,
            key=get_attempt_timestamp,
        )

    return sorted_attempts_by_ip