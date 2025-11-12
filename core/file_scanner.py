import yaml
import os

def load_config_file(config_path):
    """
    Safely loads a configuration file into a string.
    Returns the content or None if an error occurs.
    """
    if not os.path.exists(config_path):
        # This is a common case, not necessarily a critical error
        print(f"  [i] Config file not found: {config_path}")
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return f.read()
    except PermissionError:
        raise PermissionError(f"Permission denied while reading: {config_path}")
    except IOError as e:
        raise IOError(f"Error reading file {config_path}: {e}")

def load_rules_file(rules_path):
    """
    Loads and parses a YAML rules file.
    Returns the rules list or None if an error occurs.
    """
    if not os.path.exists(rules_path):
        print(f"  [!] Rules file not found: {rules_path}")
        return None
        
    try:
        with open(rules_path, 'r', encoding='utf-8') as f:
            rules = yaml.safe_load(f)
            return rules.get('rules', [])
    except yaml.YAMLError as e:
        print(f"  [!] Error parsing YAML rules file {rules_path}: {e}")
        return None
    except IOError as e:
        print(f"  [!] Error reading rules file {rules_path}: {e}")
        return None
