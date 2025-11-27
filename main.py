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
    
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        "-s", "--services", 
        nargs="+", 
        help="List of services to check (e.g. ssh nginx mysql)"
    )
    
    group.add_argument(
        "-a", "--all", 
        action="store_true", 
        help="Automatically scan ALL services found in the configs folder"
    )
    
    parser.add_argument(
        "-o", "--output", 
        default="audit_report.html", 
        help="Output filename for the HTML report"
    )

    args = parser.parse_args()

    # 2. Path Setup (Robust Fix)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "configs")
    template_path = os.path.join(base_dir, "templates")

    # 3. Handle "--all" Logic
    services_to_scan = []

    if args.all:
        if os.path.exists(config_path):
            # List all .yaml files and remove the extension to get service names
            files = [f for f in os.listdir(config_path) if f.endswith(".yaml")]
            services_to_scan = [f.replace(".yaml", "") for f in files]
            print(f"[*] Auto-detected {len(services_to_scan)} services: {', '.join(services_to_scan)}")
        else:
            print(f"[-] Error: Config directory not found at {config_path}")
            sys.exit(1)
    else:
        services_to_scan = args.services

    # 4. Initialize Engine
    engine = AuditEngine(config_dir=config_path)
    
    # 5. Run Audit
    scan_results = engine.run_audit(services_to_scan)

    # 6. Generate Report
    if scan_results:
        reporter = HTMLReporter(template_dir=template_path)
        reporter.generate(scan_results, output_file=args.output)
    else:
        print("[-] No results to report.")

if __name__ == "__main__":
    main()
```

### 🚀 How to use it

**Scan everything (The new way):**
```bash
python main.py --all
```

**Scan specific services (The old way):**
```bash
python main.py --services ssh nginx
