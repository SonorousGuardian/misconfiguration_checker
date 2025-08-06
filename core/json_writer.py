import json

def write_json_report(data, output_path):
    try:
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"[+] JSON report written to {output_path}")
    except Exception as e:
        print(f"[!] Failed to write JSON report: {e}")
