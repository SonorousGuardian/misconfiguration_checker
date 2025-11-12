import os
from datetime import datetime

# <-- CHANGED: Updated CSS for a cleaner look and new elements
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Misconfiguration Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            background: #f9fafb;
            color: #1f2937;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
            overflow: hidden; /* To contain border-radius */
        }
        header {
            padding: 20px 30px;
            border-bottom: 1px solid #e5e7eb;
            background: #f9fafb;
        }
        header h1 {
            margin: 0;
            color: #111827;
            font-size: 24px;
        }
        .metadata {
            padding: 15px 30px;
            background: #fdfdfd;
            border-bottom: 1px solid #e5e7eb;
            font-size: 14px;
            color: #4b5563;
        }
        .metadata p {
            margin: 4px 0;
        }
        .metadata strong {
            color: #374151;
        }
        .content {
            padding: 30px;
        }
        .service {
            margin-bottom: 30px;
        }
        .service h2 {
            font-size: 20px;
            color: #111827;
            border-bottom: 2px solid #d1d5db;
            padding-bottom: 8px;
            margin-top: 0;
        }
        .service-info {
            font-size: 14px;
            color: #4b5563;
            margin-bottom: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            overflow: hidden;
        }
        th, td {
            border: 1px solid #e5e7eb;
            padding: 12px 15px;
            text-align: left;
            font-size: 14px;
        }
        th {
            background-color: #f9fafb;
            color: #374151;
            font-weight: 600;
        }
        td {
            color: #374151;
        }
        tr:nth-child(even) {
            background-color: #fdfdfd;
        }
        /* Severity Classes */
        .low { background-color: #dcfce7; }
        .medium { background-color: #fef9c3; }
        .high { background-color: #fee2e2; }
        .critical { 
            background-color: #fecdd3; 
            font-weight: 600; 
            color: #991b1b; 
        }
        .unknown { background-color: #e5e7eb; }
        
        .error-box {
            background: #fff1f2;
            border: 1px solid #ffdde0;
            color: #9f1239;
            padding: 15px;
            border-radius: 6px;
        }
        .error-box strong {
            color: #9f1239;
        }
        .no-findings {
            color: #4b5563;
            font-style: italic;
            padding: 10px;
            background: #f9fafb;
            border: 1px dashed #d1d5db;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ Misconfiguration Security Report</h1>
        </header>
        
        <!-- CHANGED: Added Metadata block -->
        {metadata_content}
        
        <div class="content">
            <!-- CHANGED: Main findings content -->
            {findings_content}
        </div>
    </div>
</body>
</html>
"""

def generate_html_report(report_data, output_path="reports/report.html"):
    
    metadata_content = ""
    findings_content = ""
    
    # --- CHANGED: Generate Metadata Content ---
    metadata = report_data.get("scan_metadata", {})
    scan_time = metadata.get("scan_timestamp_utc", "Unknown Time")
    
    # Try to parse the timestamp for friendly formatting
    try:
        scan_time_obj = datetime.fromisoformat(scan_time.replace("Z", "+00:00"))
        scan_time_friendly = scan_time_obj.strftime('%Y-%m-%d %H:%M:%S %Z')
    except (ValueError, TypeError):
        scan_time_friendly = str(scan_time) # Fallback

    services_scanned = ", ".join(metadata.get('services_scanned', ['N/A']))
    
    metadata_content = (
        f"<div class='metadata'>"
        f"<p><strong>Scan Date:</strong> {scan_time_friendly}</p>"
        f"<p><strong>Services Scanned:</strong> {services_scanned}</p>"
        f"</div>"
    )

    # --- CHANGED: Generate Findings Content ---
    # Get the list of results from the main dictionary
    results_list = report_data.get("scan_results", [])
    
    if not results_list:
        findings_content = "<p class='no-findings'>No services were scanned or no results were returned.</p>"

    for result in results_list:
        # Use .get() for safe access
        service = result.get("service", "Unknown Service")
        
        section = f"<div class='service'>"
        section += f"<h2>🔧 Service: {service.upper()}</h2>"

        # --- CHANGED: Handle error state ---
        if result.get("status") == "error":
            error_msg = result.get("error_message", "An unknown error occurred.")
            section += f"<div class='error-box'>"
            section += f"<p><strong>Scan Status:</strong> Failed</p>"
            section += f"<p><strong>Error:</strong> {error_msg}</p>"
            section += "</div>"
        else:
            # --- Handle normal findings ---
            config_file = result.get("config_file", "N/A (Dynamic Check)")
            findings = result.get("findings", [])
            
            section += f"<p class='service-info'><strong>Configuration file:</strong> {config_file}</p>"

            if not findings:
                section += "<p class='no-findings'>No misconfigurations found.</p>"
            else:
                section += "<table>"
                section += "<tr><th>ID</th><th>Name</th><th>Severity</th><th>Description</th></tr>"

                for finding in findings:
                    # Use .get() for safe access
                    severity = finding.get("severity", "unknown").lower()
                    row_class = severity if severity in ["low", "medium", "high", "critical"] else "unknown"
                    
                    section += (
                        f"<tr class."'{row_class}'>"
                        f"<td>{finding.get('id', 'N/A')}</td>"
                        f"<td>{finding.get('name', 'N/A')}</td>"
                        f"<td>{finding.get('severity', 'UNKNOWN').upper()}</td>"
                        f"<td>{finding.get('description', 'N/A')}</td>"
                        f"</tr>"
                    )
                section += "</table>"
        
        section += "</div>"
        findings_content += section

    # --- CHANGED: Format the final HTML with both new blocks ---
    final_html = HTML_TEMPLATE.format(
        metadata_content=metadata_content, 
        findings_content=findings_content
    )

    # --- CHANGED: Removed os.makedirs() ---
    # This logic is now handled in main.py before this function is called.
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"[+] HTML report generated at: {output_path}")
    except IOError as e:
        print(f"[!] Error writing HTML report to {output_path}: {e}")
