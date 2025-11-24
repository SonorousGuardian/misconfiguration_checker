# GRC Compliance & Misconfiguration Scanner

Overview

A modular Compliance-as-Code framework designed to automate security auditing for Linux infrastructure. Unlike static scanners, this tool maps technical misconfigurations directly to NIST 800-53, CIS Benchmarks, and ISO 27001 controls.

It decouples validation logic (Python) from security policies (YAML), allowing GRC teams to update audit criteria without modifying the codebase.

 Key Features

Framework Mapping: Every check is tagged with relevant compliance controls (e.g., NIST AC-6, CIS 5.2).

Modular Architecture: Service-agnostic engine; supports SSH, NGINX, MySQL, Docker, and more via simple YAML plugins.

Executive Reporting: Generates professional HTML dashboards using Jinja2 for audit evidence.

DevSecOps Ready: Fully containerized with Docker for consistent scanning across environments.

 Architecture

The system uses a "Rule Engine" pattern to separate logic from policy:

graph LR
    A[YAML Configs] -->|Rules & Standards| B(Audit Engine)
    B -->|Execute System Commands| C{Host System}
    C -->|Return Shell Output| B
    B -->|Process Compliance Data| D[Jinja2 Reporter]
    D -->|Generate| E[HTML Audit Report]


🛠️ Installation & Usage

Method 1: Python (Local)

Clone the repository:

git clone [https://github.com/SonorousGuardian/misconfiguration_checker.git](https://github.com/SonorousGuardian/misconfiguration_checker.git)
cd misconfiguration_checker


Install dependencies:

pip install -r requirements.txt

## Run a scan:

# Scan specific services
python main.py --services ssh nginx mysql

# Scan all configured services (if supported by shell expansion)
python main.py --services ssh ftp dns mysql redis


Method 2: Docker (Containerized)

This tool is container-ready to ensure isolation.

# Build the image
docker build -t grc-scanner .

# Run the scanner 
# (Note: We mount the host /etc config to scan the actual system configuration)
docker run -v /etc:/etc:ro -v $(pwd)/reports:/app/reports grc-scanner


📊 Sample Output

The tool generates an interactive audit_report.html file in the root directory.

Control ID

Severity

Compliance

Status

Check Details

SSH-001

CRITICAL

NIST AC-6

<span style="color:green">PASS</span>

PermitRootLogin no

SSH-002

HIGH

CIS 5.2

<span style="color:red">FAIL</span>

PasswordAuthentication no

🧩 Adding New Rules

Rules are defined in configs/service_name.yaml. You do not need to write Python code to add a check.

Example: Adding a check for Python version

- id: "SYS-001"
  name: "Check Python Version"
  description: "Ensure Python 3 is installed."
  command: "python3 --version"
  expected: "Python 3"
  severity: "LOW"
  compliance:
    nist: "SI-2"


⚠️ Disclaimer

This tool executes system commands (grep, stat, etc.) to verify configurations. While it is designed to be read-only, it should always be run with appropriate permissions and authorization on systems you own or are authorized to audit.

Built by Amritesh Shrivastava
