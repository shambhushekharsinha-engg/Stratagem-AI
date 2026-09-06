import json
with open('skim_logs.json') as f: data = json.load(f)

def safe_get(d, k, default=0):
    return d.get(k, default) if d else default

print("--- P1 LOSS ---")
steps = data['p1_loss']
for i in range(max(0, len(steps)-10), len(steps)):
    obs = steps[i][0]['observation']
    if 'select' in obs and obs['select']:
        print(i, 'select type:', obs['select'].get('type'), 'options:', [o.get('type') for o in obs['select'].get('option', [])])
    
    c0 = obs['current']['players'][0]
    c1 = obs['current']['players'][1]
    a0 = c0.get('active', [{}])[0] if c0.get('active') else {}
    a1 = c1.get('active', [{}])[0] if c1.get('active') else {}
    
    print(f'STEP {i} -> P0 HP: {safe_get(a0, "hp")} Dmg: {safe_get(a0, "damage")}')
    print(f'          P1 HP: {safe_get(a1, "hp")} Dmg: {safe_get(a1, "damage")}')
    print(f'          P1 Status: {steps[i][1]["status"]} | Action: {steps[i][1].get("action")}')
