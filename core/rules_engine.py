import re

def check_rules(config_text,rules):
    matched_rules=[]
    
    for rule in rules:
        pattern = rule.get("match")

        if not pattern:
            continue

        try:
            if re.serach(pattern,config_text,re.IGNORECASE):
                matched_rules.append({
                    "id":rule["id"],
                    "name":rule["name"],
                    "description":rule["description"],
                    "severity":rule["severity"]
                })

        except re.error as e:
            print(f"f[!] Invalid regex in rule {rule.get('id')}:{e}")

    return matched_rules