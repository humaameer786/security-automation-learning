from threat_intel_enricher.validator import validate_ip

def main() -> None:
    ip_address = input("Enter an IP address: ")
    
    try:
        validated_ip = validate_ip(ip_address)
    except ValueError as error:
        print(error)
        return

    print(f"Valid IP address: {validated_ip}")


if __name__ == "__main__":
    main()