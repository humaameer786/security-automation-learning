from threat_intel_enricher.client import get_ip_report, VirusTotalAPIError
from threat_intel_enricher.config import load_api_key
from threat_intel_enricher.validator import validate_ip
from threat_intel_enricher.parser import parse_ip_report

def main() -> None:
    ip_address = input("Enter an IP address: ")

    try:
        validated_ip = validate_ip(ip_address)

        api_key = load_api_key()

        report = get_ip_report(
            validated_ip,
            api_key
        )
        
        threat_info = parse_ip_report(
            report
        )

    except (VirusTotalAPIError, ValueError) as error:
        print(error)
        return

    print("\nThreat intelligence report")
    print("--------------------------")

    print(f"IP address: {threat_info['ip_address']}")
    print(f"Country: {threat_info['country']}")
    print(f"ASN: {threat_info['asn']}")
    print(f"AS owner: {threat_info['as_owner']}")
    print(f"Reputation: {threat_info['reputation']}")
    print(f"Malicious detections: {threat_info['malicious']}")
    print(f"Suspicious detections: {threat_info['suspicious']}")
    print(f"Harmless detections: {threat_info['harmless']}")
    print(f"Undetected: {threat_info['undetected']}")


if __name__ == "__main__":
    main()