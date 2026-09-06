import sys
sys.path.append('C:\\Stratagem-AI')
from kaggle_environments import make
import json

def active_dump_agent(obs, config):
    if obs.step == 0:
        return [916]*4 + [1]*56
    
    select = obs.get('select', {})
    if select.get('type') in [1, 9]:
        return [0]
        
    my_idx = obs.current.get('yourIndex', 0)
    my_state = obs.current.get('players', [{}, {}])[my_idx]
    my_active = (my_state.get('active') or [None])[0]
    
    if my_active and obs.step > 0:
        with open('C:\\Stratagem-AI\\my_active_dump.txt', 'w') as f:
            f.write(json.dumps(my_active, indent=2))
        raise Exception("STOP")
            
    return [0]

env = make('cabt', debug=False)
try:
    env.run([active_dump_agent, active_dump_agent])
except Exception:
    pass
