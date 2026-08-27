import os
from kaggle_environments import make
import random

def random_agent(obs, config):
    if obs.step == 0:
        return [22]*4 + [1]*56
    
    select = obs.get('select', {})
    
    if obs.step == 1:
        print(f"Select object keys: {list(select.keys()) if select else None}")
        
    # How to make a valid random move?
    # cabt actions: list of integers.
    # usually, select has 'options', e.g. select['options'] or maybe select is a list?
    if isinstance(select, dict) and 'options' in select:
        options = select['options']
        if options:
            return [random.randrange(len(options))]
    
    return [0]

env = make('cabt', debug=True)
steps = env.run([random_agent, random_agent])
print(f'Match steps: {len(steps)}')
