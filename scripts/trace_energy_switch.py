import json
import os
import sys
from kaggle_environments import make

sys.path.append('C:\\Stratagem-AI')
from heuristic_agent import HeuristicAgent
from greedy_agent import greedy_agent

RIGGED_DECK = [96]*15 + [916]*15 + [1]*15 + [1116]*15

out_log = []
def log(s):
    out_log.append(s)

class TraceAgent(HeuristicAgent):
    def __init__(self):
        super().__init__()
        self.tracking_eswitch = False
        self.eswitch_step = 0

    def __call__(self, obs, config):
        if obs.step == 0: return RIGGED_DECK
        
        select = obs.get('select', {})
        current = obs.get('current', {})
        p = current.get('players', [{}, {}])[0]
        
        if self.tracking_eswitch and self.eswitch_step == 2 and select.get('type') == 0:
            log('\n--- AFTER ENERGY SWITCH ---')
            log(f"Active: {p.get('active', {}).get('id')} Energies: {len(p.get('active', {}).get('energies', []))}")
            for b in p.get('bench', []):
                if b: log(f"Bench: {b.get('id')} Energies: {len(b.get('energies', []))}")
            
            with open('eswitch_actual_trace.txt', 'w') as f:
                f.write('\n'.join(out_log))
            os._exit(0)
            
        if select.get('type') == 0:
            options = select.get('option', [])
            for i, opt in enumerate(options):
                hand = p.get('hand', [])
                idx = opt.get('index')
                if idx is not None and idx < len(hand):
                    card = hand[idx]
                    cid = card.get('id') if isinstance(card, dict) else card
                    if cid == 1116: # Energy Switch
                        active_energies = len(p.get('active', {}).get('energies', []))
                        bench_energies = sum(len(b.get('energies', [])) for b in p.get('bench', []) if b)
                        # We need at least one energy on the board to play it
                        if active_energies > 0 or bench_energies > 0:
                            log('\n--- BEFORE ENERGY SWITCH ---')
                            log(f"Active: {p.get('active', {}).get('id')} Energies: {active_energies}")
                            for b in p.get('bench', []):
                                if b: log(f"Bench: {b.get('id')} Energies: {len(b.get('energies', []))}")
                            self.tracking_eswitch = True
                            self.eswitch_step = 0
                            
                            res = super().__call__(obs, config)
                            log(f'Played Energy Switch: Option index {res[0]}')
                            return res
                            
        if self.tracking_eswitch and select.get('type') not in [0, 1, 9]:
            self.eswitch_step += 1
            log(f'\n--- ENERGY SWITCH PROMPT {self.eswitch_step} ---')
            log(json.dumps(select, indent=2))
            res = super().__call__(obs, config)
            log(f'Agent chose index: {res[0]}')
            log(f'Selected option: {json.dumps(select.get("option", [])[res[0]], indent=2)}')
            return res
            
        return super().__call__(obs, config)

agent_instance = TraceAgent()
def agent(obs, config): return agent_instance(obs, config)

env = make('cabt', debug=False)
for _ in range(50):
    try:
        env.run([agent, greedy_agent])
    except Exception as e:
        pass
