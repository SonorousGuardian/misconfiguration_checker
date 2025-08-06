import os
import yaml
from core.rules_engine import check_rules
from core.file_scanner import load_config_file

def run_dns_checks():
    config_path = "/etc/bind/named.conf.options"
    rule_path = "configs/dns_rules.yaml"
    config_content = load_config_file(config_path)

    with open(rule_path, "r") as f:
        rules = yaml.safe_load(f)

    matches = check_rules(config_content, rules)
    
    return {
        "service": "dns",
        "config_file": config_path,
        "findings": matches
    }
