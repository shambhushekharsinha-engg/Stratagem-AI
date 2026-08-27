import json
import sys
sys.path.append('C:\\Stratagem-AI')
from heuristic_agent import HeuristicAgent

agent = HeuristicAgent()

# 1. Main Phase: Play Energy Switch
obs_play = {
    'step': 7,
    'select': {
        'type': 0,
        'option': [{'type': 11, 'index': 0}] # Playing card from hand index 0 (Energy Switch)
    },
    'current': {
        'players': [{
            'hand': [{'id': 1116}], # Energy Switch
            'active': {'id': 96, 'energies': [1, 1]}, # Ogerpon with 2 energies
            'bench': [{'id': 916, 'energies': [1]}] # Scyther with 1 energy
        }]
    }
}

class Obs:
    def __init__(self, d):
        self.step = d['step']
        self.select = d['select']
        self.current = d['current']
    def get(self, key, default=None):
        return getattr(self, key, default)

obs_play_obj = Obs(obs_play)
res = agent(obs_play_obj, {})
print("Pending Action state:", agent.pending_action)

# 2. Prompt 1: Take FROM
obs_prompt1 = {
    'step': 8,
    'select': {
        'type': 4, # Target selection
        'minCount': 1,
        'option': [
            {'area': 4, 'index': 0}, # Active Ogerpon
            {'area': 5, 'index': 0}  # Bench Scyther
        ]
    },
    'current': obs_play['current']
}

print("\n--- 2. PROMPT 1: TAKE FROM ---")
print(json.dumps(obs_prompt1['select'], indent=2))
res1 = agent(obs_prompt1, {})
print("Agent chose index:", res1[0])
print("Selected Option:", obs_prompt1['select']['option'][res1[0]])
print("Pending Action state:", agent.pending_action)

# 3. Prompt 2: Give TO
obs_prompt2 = {
    'step': 9,
    'select': {
        'type': 4,
        'minCount': 1,
        'option': [
            {'area': 4, 'index': 0}, # Active Ogerpon
            {'area': 5, 'index': 0}  # Bench Scyther
        ]
    },
    'current': obs_play['current']
}

print("\n--- 3. PROMPT 2: GIVE TO ---")
print(json.dumps(obs_prompt2['select'], indent=2))
res2 = agent(obs_prompt2, {})
print("Agent chose index:", res2[0])
print("Selected Option:", obs_prompt2['select']['option'][res2[0]])
print("Pending Action state:", agent.pending_action)

# 4. Return to Main Phase
obs_return = {
    'step': 10,
    'select': {'type': 0, 'option': []},
    'current': obs_play['current']
}
print("\n--- 4. RETURN TO MAIN PHASE ---")
agent(obs_return, {})
print("Pending Action state:", agent.pending_action)
