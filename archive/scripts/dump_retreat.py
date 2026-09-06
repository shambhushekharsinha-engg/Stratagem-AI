import json
with open('excerpt_match.json') as f: steps = json.load(f)

for i in range(98, 103):
    obs = steps[i][0]['observation']
    p0 = steps[i][0]
    p1 = steps[i][1]
    
    if 'select' in obs and obs['select']:
        opts = obs['select']['option']
        print(f'\n--- STEP {i} ---')
        
        c0 = obs['current']['players'][0]
        c1 = obs['current']['players'][1]
        a0 = c0.get('active', [{}])[0] if c0.get('active') else {}
        a1 = c1.get('active', [{}])[0] if c1.get('active') else {}
        
        print(f'P0 (Heur) HP: {a0.get("hp",0)} Dmg: {a0.get("damage",0)} Energies: {len(a0.get("energies",[]))} ID: {a0.get("id")}')
        print(f'P1 (Grdy) HP: {a1.get("hp",0)} Dmg: {a1.get("damage",0)} Energies: {len(a1.get("energies",[]))} ID: {a1.get("id")}')
        
        print(f'Options: {[o.get("type") for o in opts]}')
        
        act0 = p0.get("action")
        if act0 and act0[0] < len(opts):
            chosen = opts[act0[0]]
            print(f'P0 Action {act0}: Type {chosen.get("type")}')
        else:
            print(f'P0 Action {act0}')
            
        act1 = p1.get("action")
        print(f'P1 Action {act1}')
