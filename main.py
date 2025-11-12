import argparse
import json
import os
from datetime import datetime
# We will use this now!

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
    "low": "\033[92m",      # Green
    "medium": "\033[93m",   # Yellow
    "high": "\033[91m",     # Red
    "critical": "\033[95m"   # Magenta
}

RESET_COLOR = "\033[0m"

def color_text(text, severity):
    # <-- FIX: Added .lower() and a default .get() for safety
    color = SEVERITY_COLORS.get(str(severity).lower(), "")
    return f"{color}{text}{RESET_COLOR}"

def main():
    parser = argparse.ArgumentParser(description="🛡️ Modular Misconfiguration Checker")

    # <-- IMPROVEMENT: Create a timestamp for default filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_json_path = f"reports/report_{timestamp}.json"
    default_html_path = f"reports/report_{timestamp}.html"

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
        default=default_json_path,  # <-- IMPROVEMENT: Use timestamped default
        help=f"Output path for JSON report (default: {default_json_path})"
    )

    parser.add_argument(
        "-H", "--html", 
        default=default_html_path,  # <-- IMPROVEMENT: Use timestamped default
        help=f"Output path for HTML report (default: {default_html_path})"
    )

    args = parser.parse_args()

    if not args.services and not args.all:
        parser.error("Please specify at least one service using --services or use --all")

    selected_services = SERVICE_MAP.keys() if args.all else args.services
    
    # <-- IMPROVEMENT: Create a full report object with metadata
    scan_start_time = datetime.now()
    report_data = {
        "scan_metadata": {
            "scan_timestamp_utc": scan_start_time.isoformat(),
            "services_scanned": list(selected_services)
        },
        "scan_results": []
    }
    
    print(f"Starting scan at {scan_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    for service in selected_services:
        print(f"[+] Checking {service.upper()} configuration...")
        try:
            checker = SERVICE_MAP[service]
            result = checker()

            # <-- FIX: Use .get() for safe access. Check for None result.
            if result and result.get("findings"):
                report_data["scan_results"].append(result) # Add to our new report object
                for finding in result["findings"]:
                    # <-- FIX: Use .get() for safe severity access
                    severity = finding.get("severity", "unknown") 
                    colored_severity = color_text(severity.upper(), severity)
                    
                    # <-- FIX: Use .get() for safe name/description access
                    name = finding.get("name", "Unnamed Finding")
                    desc = finding.get("description", "No description provided.")
                    print(f"  - {name} [{colored_severity}]: {desc}")
                print()
            else:
                print("  → No misconfigurations found.\n")
        
        # <-- FIX: Catch exceptions from a failing module
        except Exception as e:
            print(f"  [!] ERROR scanning {service}: {e}\n")
            # Optionally, you could add this error to the report
            report_data["scan_results"].append({
                "service": service,
                "status": "error",
                "error_message": str(e),
                "findings": []
            })


    if report_data["scan_results"]:
        # <-- FIX: Safely create report directories
        json_dir = os.path.dirname(args.json)
        html_dir = os.path.dirname(args.html)

        if json_dir: # Only create if path is not empty
            os.makedirs(json_dir, exist_ok=True)
        if html_dir and html_dir != json_dir: # Only create if not empty and not the same as json_dir
             os.makedirs(html_dir, exist_ok=True)

        # <-- IMPROVEMENT: Pass the full report_data object
        write_json_report(report_data, args.json)
        generate_html_report(report_data, args.html)
        print(f"\n✅ Reports saved: {args.json}, {args.html}")
    else:
        print("\n✅ No misconfigurations found in the selected services.")

if __name__ == "__main__":
    main()
