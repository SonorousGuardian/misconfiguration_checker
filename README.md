# GRC Compliance & Misconfiguration Scanner

## Overview

A modular Compliance-as-Code framework mapping Linux misconfigurations directly to NIST 800-53, CIS Benchmarks, and ISO 27001 controls. It decouples validation logic (Python) from security policies (YAML), allowing GRC teams to update audit criteria without code changes.

## Key Features

Framework Mapping: Checks are tagged with controls (e.g., NIST AC-6, CIS 5.2).

Modular Architecture: Service-agnostic engine supports SSH, NGINX, MySQL, etc. via YAML.

Executive Reporting: Generates professional HTML dashboards using Jinja2.

## Architecture

The system uses a "Rule Engine" pattern to separate logic from policy:

graph LR
    A[YAML Configs] -->|Rules & Standards| B(Audit Engine)
    B -->|Execute System Commands| C{Host System}
    C -->|Return Shell Output| B
    B -->|Process Compliance Data| D[Jinja2 Reporter]
    D -->|Generate| E[HTML Audit Report]


## Installation & Usage

Clone the repository:

git clone [https://github.com/SonorousGuardian/misconfiguration_checker.git](https://github.com/SonorousGuardian/misconfiguration_checker.git)
cd misconfiguration_checker


Install dependencies:

pip install -r requirements.txt


Run a scan:

# Scan specific services
python main.py --services ssh nginx mysql

# Scan all configured services
python main.py --services ssh ftp dns mysql redis


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

Rules are defined in configs/service_name.yaml. No coding required.

Example:

- id: "SYS-001"
  name: "Check Python Version"
  description: "Ensure Python 3 is installed."
  command: "python3 --version"
  expected: "Python 3"
  severity: "LOW"
  compliance:
    nist: "SI-2"


⚠️ Disclaimer

This tool executes system commands (grep, stat, etc.) to verify configurations. Ensure you have authorization to audit the target systems.

Built by Amritesh Shrivastava
