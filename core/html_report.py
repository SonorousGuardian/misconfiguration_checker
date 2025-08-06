import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Misconfiguration Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            padding: 20px;
        }}
        h1 {{
            color: #333;
        }}
        .service {{
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #eee;
        }}
        .low {{ background-color: #d4edda; }}
        .medium {{ background-color: #fff3cd; }}
        .high {{ background-color: #f8d7da; }}
        .critical {{ background-color: #f5c6cb; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>🛡️ Misconfiguration Security Report</h1>
    {content}
</body>
</html>
"""

def generate_html_report(results, output_path="reports/report.html"):
    content = ""
    
    for result in results:
        service = result["service"]
        config_file = result["config_file"]
        findings = result["findings"]

        section = f"<div class='service'>"
        section += f"<h2>🔧 Service: {service.upper()}</h2>"
        section += f"<p><strong>Configuration file:</strong> {config_file}</p>"
        section += "<table>"
        section += "<tr><th>ID</th><th>Name</th><th>Severity</th><th>Description</th></tr>"

        for finding in findings:
            severity = finding["severity"].lower()
            row_class = severity if severity in ["low", "medium", "high", "critical"] else ""
            section += (
                f"<tr class='{row_class}'>"
                f"<td>{finding['id']}</td>"
                f"<td>{finding['name']}</td>"
                f"<td>{finding['severity'].upper()}</td>"
                f"<td>{finding['description']}</td>"
                f"</tr>"
            )

        section += "</table></div>"
        content += section

    final_html = HTML_TEMPLATE.format(content=content)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(final_html)
    
    print(f"[+] HTML report generated at: {output_path}")
