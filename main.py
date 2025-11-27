import argparse
import os
import sys
from core.engine import AuditEngine
from core.reporter import HTMLReporter

def main():
    # 1. Setup Argument Parser
    parser = argparse.ArgumentParser(
        description="GRC Compliance Checker: Automated Audit Tool mapped to NIST/CIS"
    )
    
    parser.add_argument(
        "-s", "--services", 
        nargs="+", 
        default=["ssh", "nginx", "mysql"], 
        help="List of services to check (e.g. ssh nginx mysql)"
    )
    
    parser.add_argument(
        "-o", "--output", 
        default="audit_report.html", 
        help="Output filename for the HTML report"
    )

    args = parser.parse_args()

    # --- FIX START ---
    # Get the absolute path of the directory where main.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the absolute path to the configs folder
    config_path = os.path.join(base_dir, "configs")
    template_path = os.path.join(base_dir, "templates")

    print(f"[*] Debug: Looking for configs in: {config_path}")
    # --- FIX END ---

    # 2. Initialize the Engine with the absolute path
    engine = AuditEngine(config_dir=config_path)
    
    # 3. Run the Audit
    scan_results = engine.run_audit(args.services)

    # 4. Generate the Report
    if scan_results:
        # Pass the absolute template path to reporter
        reporter = HTMLReporter(template_dir=template_path)
        reporter.generate(scan_results, output_file=args.output)
    else:
        print("[-] No results to report.")

if __name__ == "__main__":
    main()
