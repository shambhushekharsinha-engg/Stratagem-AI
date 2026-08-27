import json, sys
sys.path.append('C:\\Stratagem-AI')
from heuristic_agent import HeuristicAgent

with open('excerpt_match.json') as f: match = json.load(f)

agent = HeuristicAgent()
class Obs:
    def __init__(self, step, obs):
        self.step = step
        self.select = obs.get('select', {})
        self.current = obs.get('current', {})
    def get(self, k, d=None): return getattr(self, k, d)

# We will patch the agent's internal functions to print when they fire
original_call = agent.__call__

def wrap_call(obs, conf):
    # Just run it and see if we can infer what happened
    pass

for i in range(len(match)-1):
    obs = match[i][0]['observation']
    if 'select' in obs and obs['select']:
        # Let's inspect the agent's internal decisions by running it up to this point
        pass
