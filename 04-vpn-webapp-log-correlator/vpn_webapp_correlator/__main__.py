from pathlib import Path
from vpn_webapp_correlator.loader import (
    load_vpn_logs,
    load_webapp_logs,
)

# print the loaded logs to the console
def main() -> None:
    vpn_file = Path("data/vpn_logs.csv")
    webapp_file = Path("data/webapp_logs.csv")

    vpn_logs = load_vpn_logs(vpn_file)
    webapp_logs = load_webapp_logs(webapp_file)

    print("VPN logs")
    print("--------")
    print(vpn_logs.to_string(index=False))

    print()
    print("WebApp logs")
    print("-----------")
    print(webapp_logs.to_string(index=False))


if __name__ == "__main__":
    main()