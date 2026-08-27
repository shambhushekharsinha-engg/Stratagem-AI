import sys
sys.path.append('C:\\Stratagem-AI')
from heuristic_agent import HeuristicAgent

agent = HeuristicAgent()

class O:
    def __init__(self, d): self.d = d
    def get(self, k, default=None): return self.d.get(k, default)
    @property
    def step(self): return self.d.get('step', 0)
    @property
    def select(self): return self.d.get('select', {})
    @property
    def current(self): return self.d.get('current', {})

print("--- PRIORITY 1: LETHAL KO TRACE ---")
# Board: Ogerpon ex (4 energies) vs Active Ogerpon ex (210 HP). Bench has Scyther (20 HP remaining). 
# My prizes: 1. Scyther gives 1 prize. Lethal KO on Bench via Boss!
obs_p1 = {
    'step': 10,
    'select': {'type': 0, 'option': [{'type': 13, 'attackId': 100}, {'type': 12, 'index': 0}]},
    'current': {
        'yourIndex': 0,
        'players': [
            {
                'active': [{'id': 96, 'hp': 210, 'energies': [1,1,1,1]}],
                'hand': [{'id': 1182}], # Boss
                'prize': [{'id': 1}] # 1 prize left!
            },
            {
                'active': [{'id': 96, 'hp': 210, 'energies': []}],
                'bench': [{'id': 916, 'hp': 20, 'energies': []}]
            }
        ]
    }
}

act_p1 = agent(O(obs_p1), None)
print("Step 1 (Main Phase) returned index:", act_p1)
print("Pending Action:", getattr(agent, 'pending_action', None))


print("\\n--- PRIORITY 3: ACTIVE KO TRACE ---")
# Board: Ogerpon ex (4 energies, 150 dmg potential) vs Active Scyther (70 HP). My prizes: 6 (not lethal).
# Should directly attack and KO the active Scyther without using Boss's Orders.
obs_p3 = {
    'step': 12,
    'select': {'type': 0, 'option': [{'type': 13, 'attackId': 1321}, {'type': 12, 'index': 0}]},
    'current': {
        'yourIndex': 0,
        'players': [
            {
                'active': [{'id': 96, 'hp': 210, 'energies': [1,1,1,1]}],
                'hand': [{'id': 1182}], # Boss
                'prize': [{'id': 1}] * 6 # 6 prizes left
            },
            {
                'active': [{'id': 916, 'hp': 70, 'energies': []}],
                'bench': [{'id': 96, 'hp': 210, 'energies': []}]
            }
        ]
    }
}
agent.pending_action = None # Reset
act_p3 = agent(O(obs_p3), None)
print("Step 1 (Main Phase) returned index:", act_p3)
print("Priority 3 returned option type:", obs_p3['select']['option'][act_p3[0]]['type'])

