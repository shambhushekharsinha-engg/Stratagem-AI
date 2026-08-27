import sys
sys.path.append('C:\\Stratagem-AI')
from heuristic_agent import HeuristicAgent

agent = HeuristicAgent()

# Step 1: Main phase, Boss's Orders in hand
obs1 = {
    'step': 10,
    'select': {
        'type': 0, 
        'option': [{'type': 13, 'attackId': 100}, {'type': 12, 'index': 0}]
    },
    'current': {
        'yourIndex': 0,
        'players': [
            {
                'active': [{'id': 96, 'hp': 210, 'energies': [1,1,1,1]}],
                'hand': [{'id': 1182}] # Boss
            },
            {
                'active': [{'id': 96, 'hp': 210, 'energies': []}],
                'bench': [{'id': 916, 'hp': 70, 'energies': []}]
            }
        ]
    }
}

class O:
    def __init__(self, d): self.d = d
    def get(self, k, default=None): return self.d.get(k, default)
    @property
    def step(self): return self.d.get('step', 0)
    @property
    def select(self): return self.d.get('select', {})
    @property
    def current(self): return self.d.get('current', {})

act1 = agent(O(obs1), None)
print("Step 1 (Main Phase) returned:", act1)
print("Pending Action:", getattr(agent, 'pending_action', None))

# Step 2: Engine prompts to select target (Type 3)
obs2 = {
    'step': 11,
    'select': {
        'type': 3, 
        'option': [{'type': 3, 'index': 0}]
    },
    'current': obs1['current']
}

act2 = agent(O(obs2), None)
print("Step 2 (Select Target) returned:", act2)
print("Pending Action:", getattr(agent, 'pending_action', None))
