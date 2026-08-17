import requests

BASE_URL = "https://www.virustotal.com/api/v3/ip_addresses"

class VirusTotalAPIError(Exception):
    pass

# request an IP address report
def get_ip_report(
    ip_address: str,
    api_key: str
) -> dict:
    try:
        response = requests.get(
            f"{BASE_URL}/{ip_address}",
            headers={
                "x-apikey": api_key,
            },
            timeout=10,
        )
    except requests.Timeout as error:
        raise VirusTotalAPIError(
            "VirusTotal request timed out."
        ) from error
    except requests.RequestException as error:
        raise VirusTotalAPIError(
            "Could not connect to VirusTotal."
        ) from error

    if response.status_code == 401:
        raise VirusTotalAPIError(
            "VirusTotal rejected the API key."
        )

    if response.status_code == 404:
        raise VirusTotalAPIError(
            "No VirusTotal report was found for this IP."
        )

    if response.status_code == 429:
        raise VirusTotalAPIError(
            "VirusTotal API rate limit reached."
        )

    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise VirusTotalAPIError(
            f"VirusTotal returned HTTP {response.status_code}."
        ) from error

    return response.json()