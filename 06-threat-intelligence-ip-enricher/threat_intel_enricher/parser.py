# extract the useful threat-intelligence fields
def parse_ip_report(report: dict) -> dict:
    data = report.get("data", {})
    attributes = data.get("attributes", {})
    stats = attributes.get(
        "last_analysis_stats",
        {},
    )

    return {
        "ip_address": data.get("id"),
        "country": attributes.get("country"),
        "asn": attributes.get("asn"),
        "as_owner": attributes.get("as_owner"),
        "reputation": attributes.get("reputation"),
        "malicious": stats.get("malicious", 0),
        "suspicious": stats.get("suspicious", 0),
        "harmless": stats.get("harmless", 0),
        "undetected": stats.get("undetected", 0),
    }