import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = PROJECT_ROOT/"data"/"cache.json"

def load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {}

    with CACHE_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)

def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with CACHE_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            cache,
            file,
            indent=4,
        )

def get_cached_report(
    ip_address: str,
) -> dict | None:
    cache = load_cache()

    return cache.get(ip_address)

def cache_report(
    ip_address: str,
    report: dict,
) -> None:
    cache = load_cache()

    cache[ip_address] = report

    save_cache(cache)