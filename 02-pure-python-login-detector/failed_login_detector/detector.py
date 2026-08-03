from datetime import datetime, timedelta

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

# Build time windows of authentication attempts for each source IP
def build_time_windows(
    ip_attempts: list[dict[str, object]],
    window_minutes: int = 5,
) -> list[list[dict[str, object]]]:
    windows = []
    window_duration = timedelta(minutes=window_minutes)

    for start_index, start_attempt in enumerate(ip_attempts):
        start_time = get_attempt_timestamp(start_attempt)
        window_end = start_time + window_duration
        current_window = []

        for attempt in ip_attempts[start_index:]:
            attempt_time = get_attempt_timestamp(attempt)

            if attempt_time <= window_end:
                current_window.append(attempt)
            else:
                break

        windows.append(current_window)

    return windows

# Analyze a time window of authentication attempts
def analyze_window(
    window: list[dict[str, object]],
) -> dict[str, int | float]:
    unique_users = {
        str(attempt["username"])
        for attempt in window
    }

    failed_attempts = sum(
        1
        for attempt in window
        if attempt["result"] == "failure"
    )

    total_attempts = len(window)

    if total_attempts == 0:
        failure_rate = 0.0
    else:
        failure_rate = failed_attempts / total_attempts

    return {
        "total_attempts": total_attempts,
        "unique_users": len(unique_users),
        "failed_attempts": failed_attempts,
        "failure_rate": failure_rate,
    }