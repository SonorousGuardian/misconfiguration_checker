import yaml
import subprocess
import os
import sys

class AuditEngine:
    def __init__(self, config_dir="configs"):
        self.config_dir = config_dir
        self.results = []

    def load_rules(self, service_name):
        """Loads YAML rules for a specific service (e.g., 'ssh')."""
        filepath = os.path.join(self.config_dir, f"{service_name}.yaml")
        
        if not os.path.exists(filepath):
            print(f"[-] Warning: Configuration file for '{service_name}' not found at {filepath}")
            return []
        
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
                return data.get('rules', [])
        except Exception as e:
            print(f"[-] Error parsing YAML for {service_name}: {e}")
            return []

    def check_rule(self, rule):
        """Runs the system command and compares output."""
        try:
            # Execute the shell command
            proc = subprocess.run(
                rule['command'], 
                shell=True, 
                text=True, 
                capture_output=True
            )
            
            actual_output = proc.stdout.strip()
            error_output = proc.stderr.strip()
            
            # Logic: Check if the expected string is inside the output
            # We use 'in' to handle varying whitespace or extra text
            if rule['expected'] in actual_output:
                status = "PASS"
            else:
                status = "FAIL"
                # If command failed (e.g., file not found), capture that error
                if proc.returncode != 0:
                    actual_output = f"Command Failed: {error_output}"

        except Exception as e:
            actual_output = f"Execution Error: {str(e)}"
            status = "ERROR"

        # Return a structured dictionary for the report
        return {
            "id": rule.get('id', 'N/A'),
            "name": rule.get('name', 'Unknown Check'),
            "severity": rule.get('severity', 'LOW'),
            "compliance": rule.get('compliance', {}), 
            "expected": rule.get('expected', ''),
            "actual": actual_output,
            "status": status
        }

    def run_audit(self, services):
        """Main loop to check all requested services."""
        print(f"[*] Starting Compliance Audit for: {', '.join(services)}")
        print("-" * 50)
        
        for service in services:
            rules = self.load_rules(service)
            if not rules:
                continue

            print(f"[*] Auditing Service: {service.upper()} ({len(rules)} checks)")
            
            for rule in rules:
                result = self.check_rule(rule)
                self.results.append(result)
                
                # Console Feedback (Green for Pass, Red for Fail)
                color = "\033[92m" if result['status'] == "PASS" else "\033[91m"
                reset = "\033[0m"
                print(f"   [{color}{result['status']}{reset}] {result['id']}: {result['name']}")

        return self.results