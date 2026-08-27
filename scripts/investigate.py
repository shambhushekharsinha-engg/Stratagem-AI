import json
import os

directory = r'C:\Stratagem-AI\data\episodes'
files = [f for f in os.listdir(directory) if f.endswith('.json')]

simultaneous = []
no_prize = []

for f_name in files:
    with open(os.path.join(directory, f_name), encoding='utf-8') as f:
        data = json.load(f)
        
    steps = data.get('steps', [])
    if len(steps) < 2: continue
    
    first_taker = None
    simul = False
    prev_l0 = None
    prev_l1 = None
    
    for i, step in enumerate(steps):
        current = step[0].get('observation', {}).get('current', {})
        if not current: continue
        
        p0 = current['players'][0].get('prize', [])
        p1 = current['players'][1].get('prize', [])
        
        l0 = len(p0) if isinstance(p0, list) else 6
        l1 = len(p1) if isinstance(p1, list) else 6
        
        if l0 == 0 or l1 == 0: continue
        
        if l0 < 6 and l1 == 6:
            first_taker = 0
            break
        elif l1 < 6 and l0 == 6:
            first_taker = 1
            break
        elif l0 < 6 and l1 < 6:
            simul = True
            if len(simultaneous) < 3:
                print(f"Simultaneous in {f_name} at step {i}.")
                print(f"  Prev step: P0={prev_l0}, P1={prev_l1}")
                print(f"  Curr step: P0={l0}, P1={l1}")
            simultaneous.append(f_name)
            break
            
        prev_l0 = l0
        prev_l1 = l1
        
    if first_taker is None and not simul:
        no_prize.append(f_name)

print(f"\nTotal Simultaneous: {len(simultaneous)}")
print(f"Total No Prize Taken: {len(no_prize)}")
if no_prize:
    print(f"Example no-prize game: {no_prize[0]}")
    with open(os.path.join(directory, no_prize[0]), encoding='utf-8') as f:
        data2 = json.load(f)
        print(f"  Step count: {len(data2.get('steps', []))}")
        print(f"  Rewards: P0={data2['steps'][-1][0].get('reward')}, P1={data2['steps'][-1][1].get('reward')}")
