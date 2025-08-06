import argparse
import json
import os
from datetime import datetime

from core.json_writer import write_json_report
from core.html_report import generate_html_report
from modules.ssh_checker import run_ssh_checks
from modules.ftp_checker import run_ftp_checks
from modules.nginx_checker import run_nginx_checks
from modules.apache_checker import run_apache_checks
from modules.mysql_checker import run_mysql_checks
from modules.smb_checker import run_smb_checks
from modules.dns_checker import run_dns_checks
from modules.snmp_checker import run_snmp_checks

# Map service name to corresponding checker function
SERVICE_MAP = {
    "ssh": run_ssh_checks,
    "ftp": run_ftp_checks,
    "nginx": run_nginx_checks,
    "apache": run_apache_checks,
    "mysql": run_mysql_checks,
    "smb": run_smb_checks,
    "dns": run_dns_checks,
    "snmp": run_snmp_checks
}

SEVERITY_COLORS = {
    "low": "\033[92m",       # Green
    "medium": "\033[93m",    # Yellow
    "high": "\033[91m",      # Red
    "critical": "\033[95m"    # Magenta
}

RESET_COLOR = "\033[0m"

def color_text(text, severity):
    color = SEVERITY_COLORS.get(severity.lower(), "")
    return f"{color}{text}{RESET_COLOR}"

def main():
    parser = argparse.ArgumentParser(description="\U0001F50D Modular Misconfiguration Checker")

    parser.add_argument(
        "-s", "--services",
        nargs="+",
        choices=SERVICE_MAP.keys(),
        help="List of services to scan (e.g., ssh ftp mysql)"
    )

    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Scan all supported services"
    )

    parser.add_argument(
        "-j", "--json", 
        default="reports/report.json", 
        help="Output path for JSON report"
    )

    parser.add_argument(
        "-H", "--html", 
        default="reports/report.html", 
        help="Output path for HTML report"
    )

    args = parser.parse_args()

    if not args.services and not args.all:
        parser.error("Please specify at least one service using --services or use --all")

    selected_services = SERVICE_MAP.keys() if args.all else args.services
    results = []

    for service in selected_services:
        print(f"[+] Checking {service.upper()} configuration...")
        checker = SERVICE_MAP[service]
        result = checker()

        if result["findings"]:
            results.append(result)
            for finding in result["findings"]:
                severity = finding["severity"]
                colored_severity = color_text(severity.upper(), severity)
                print(f"  - {finding['name']} [{colored_severity}]: {finding['description']}")
            print()
        else:
            print("  → No misconfigurations found.\n")

    if results:
        os.makedirs(os.path.dirname(args.json), exist_ok=True)
        write_json_report(results, args.json)
        generate_html_report(results, args.html)
        print(f"\n\u2705 Reports saved: {args.json}, {args.html}")
    else:
        print("\n\u2705 No misconfigurations found in the selected services.")

if __name__ == "__main__":
    main()
