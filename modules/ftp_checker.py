import os
import yaml
from core.rules_engine import check_rules
from core.file_scanner import load_config_file

def run_ftp_checks():
    config_path = "/etc/vsftpd.conf"
    rule_path = "configs/ftp_rules.yaml"
    config_content = load_config_file(config_path)

    with open(rule_path, "r") as f:
        rules = yaml.safe_load(f)

    matches = check_rules(config_content, rules)
    
    return {
        "service": "ftp",
        "config_file": config_path,
        "findings": matches
    }
