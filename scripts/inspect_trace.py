import json
with open('trace_log.json', 'r') as f:
    log = json.load(f)

for entry in log:
    if entry['select'].get('type') == 0:
        for opt in entry['select'].get('option', []):
            if opt.get('type') in [12, 13]: # Let's see what these are
                print(f"Step {entry['step']} Option: {opt}")
