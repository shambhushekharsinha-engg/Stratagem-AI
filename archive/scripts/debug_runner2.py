import os
from kaggle_environments import make
import random

def agent(obs, config):
    if obs.step == 0:
        return [96]*4 + [24]*4 + [1]*12 + [1182]*4 + [1213]*4 + [1192]*4 + [1191]*4 + [1086]*4 + [1121]*4 + [1107]*4 + [1116]*4 + [1077]*4 + [1082]*4
    
    select = obs.get('select', {})
    options = select.get('option', [])
    if options:
        return [random.randrange(len(options))]
    return []

env = make('cabt', debug=True)
steps = env.run([agent, agent])
print(f'Match steps: {len(steps)}')
for i, step in enumerate(steps[:3]):
    print(f'Step {i}:')
    for p_idx, agent_state in enumerate(step):
        status = agent_state.status
        reward = agent_state.reward
        print(f'  Agent {p_idx} status: {status}, reward: {reward}')
