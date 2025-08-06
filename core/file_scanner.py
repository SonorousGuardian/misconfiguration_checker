def load_config_file(path):

    try:
        with open(path,'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"[!] file not found:{path}")

    except PermissionError:
        print(f"[!] Permission denied when reading:{path}")

    except Exception as e:
        print(f"[!] Error reading {path}: {e}")
    
    return ""