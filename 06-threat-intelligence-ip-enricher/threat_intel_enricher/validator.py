import ipaddress

# validate IP address
def validate_ip(ip_address: str) -> str:
    try:
        validated_ip = ipaddress.ip_address(
            ip_address.strip()
        )
    except ValueError as error:
        raise ValueError(
            f"Invalid IP address: {ip_address}"
        ) from error

    return str(validated_ip)