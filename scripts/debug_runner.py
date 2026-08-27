import os
from kaggle_environments import make
import random

def random_agent(obs, config):
    options = obs.get('options', [])
    if obs.step == 0:
        return [22]*4 + [1]*56
    if not options:
        return []
    return [random.randrange(len(options))]

env = make('cabt', debug=True)
steps = env.run([random_agent, random_agent])

print(f'Match steps: {len(steps)}')
for i, step in enumerate(steps):
    print(f'Step {i}:')
    for p_idx, agent in enumerate(step):
        # agent is a dict-like object (State)
        status = agent.status
        reward = agent.reward
        print(f'  Agent {p_idx} status: {status}, reward: {reward}')
        # print action if available
        if 'action' in agent:
            print(f'  Agent {p_idx} action: {agent.action}')
