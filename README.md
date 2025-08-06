Misconfiguration Checker

A modular and extensible misconfiguration scanner for detecting insecure settings in popular infrastructure services. Built for system administrators, DevSecOps teams, and security auditors, this tool uses YAML-based rules to identify unsafe defaults and insecure configurations across various common services.

Features

🔍 Rule-based detection using YAML configuration

🧩 Modular architecture per service

📜 Human-readable JSON and HTML reports

🎨 Color-coded terminal output by severity

🔧 CLI interface for selecting services or scanning all

📂 Project Structure

misconfig_checker/
├── configs/               # YAML rule definitions for each service
├── core/                  # Core logic for rule engine, reporting
├── modules/               # Individual service scanners
├── reports/               # Output folder for reports
├── main.py                # Entry-point CLI
├── requirements.txt       # Python dependencies
└── README.md              # Project overview

✅ Supported Services

SSH

FTP

Apache

Nginx

MySQL

SMB (Samba)

DNS

SNMP

🚀 Usage

Run scan for specific services:

python main.py -s ssh ftp mysql

Scan all services:

python main.py --all

Custom output paths:

python main.py --all -j reports/output.json -H reports/output.html

📋 Output

Console: Color-coded summary with severity (Low/Medium/High/Critical)

JSON: Structured machine-readable output (reports/report.json)

HTML: Styled and color-coded HTML report (reports/report.html)

🛠 Requirements

Install dependencies:

pip install -r requirements.txt

🧱 Add Your Own Rules

Create a YAML file under configs/

Follow this format:

- id: ssh-001
  name: "Root login is enabled"
  match: "PermitRootLogin yes"
  description: "Allows root user to login over SSH."
  severity: "high"

Add a corresponding checker in modules/

