import requests

BASE_URL = "https://www.virustotal.com/api/v3/ip_addresses"

# request an IP address report
def get_ip_report(
    ip_address: str,
    api_key: str,
) -> dict:
    # make the request
    response = requests.get(
        f"{BASE_URL}/{ip_address}",
        headers={
            "x-apikey": api_key,
        },
        timeout=10,
    )
    # raise an error if the request fails
    response.raise_for_status()

    return response.json()