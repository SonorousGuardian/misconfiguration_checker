from jinja2 import Environment, FileSystemLoader
import os
import datetime

class HTMLReporter:
    def __init__(self, template_dir="templates"):
        self.template_dir = template_dir
        # Initialize Jinja2 Environment
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def generate(self, results, output_file="audit_report.html"):
        """Renders the results into the HTML template."""
        try:
            template = self.env.get_template('report.html')
            
            # Calculate stats for the dashboard
            total = len(results)
            passed = sum(1 for r in results if r['status'] == 'PASS')
            failed = sum(1 for r in results if r['status'] == 'FAIL')
            
            # Render the data
            html_content = template.render(
                results=results,
                scan_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                stats={"total": total, "passed": passed, "failed": failed}
            )
            
            # Write to file
            with open(output_file, "w") as f:
                f.write(html_content)
            
            print("\n" + "="*50)
            print(f"[+] 📄 Report generated successfully: {os.path.abspath(output_file)}")
            print("="*50)
            
        except Exception as e:
            print(f"[-] Error generating report: {e}")