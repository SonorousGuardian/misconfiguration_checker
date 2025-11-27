import argparse
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

    # 2. Initialize the Engine
    engine = AuditEngine(config_dir="configs")
    
    # 3. Run the Audit
    scan_results = engine.run_audit(args.services)

    # 4. Generate the Report
    if scan_results:
        reporter = HTMLReporter(template_dir="templates")
        reporter.generate(scan_results, output_file=args.output)
    else:
        print("[-] No results to report.")

if __name__ == "__main__":
    main()