import sys
sys.path.append('C:\\Stratagem-AI')
from kaggle_environments import make
import random

def attack_dump_agent(obs, config):
    if obs.step == 0:
        return [916]*4 + [1]*56
    
    select = obs.get('select', {})
    options = select.get('option', [])
    if not options: return []
    
    if select.get('type') in [1, 9]:
        return [0]
        
    attacks = [opt for opt in options if opt.get('type') == 13]
    if len(attacks) >= 2:
        with open('C:\\Stratagem-AI\\attack_dump.txt', 'w') as f:
            f.write(f"STEP {obs.step}: Scyther has attack options: {options}\\n")
        raise Exception("STOP")
            
    for i, opt in enumerate(options):
        if opt.get('type') == 8:
            return [i]
            
    if attacks:
        # Just pass instead of attacking so we can attach more energy!
        for i, opt in enumerate(options):
            if opt.get('type') == 14: return [i]
            
    return [0]

env = make('cabt', debug=False)
try:
    env.run([attack_dump_agent, attack_dump_agent])
except Exception:
    pass
