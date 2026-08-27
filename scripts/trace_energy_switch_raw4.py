import json
import sys
from kaggle_environments import make

sys.path.append('C:\\Stratagem-AI')
from heuristic_agent import HeuristicAgent
from greedy_agent import greedy_agent

LEGAL_RIGGED_DECK = [1116]*4 + [916]*4 + [96]*4 + [1]*48

class DumpAgent(HeuristicAgent):
    def __init__(self):
        super().__init__()
        self.played = False
        self.step_tracker = 0

    def __call__(self, obs, config):
        if obs.step == 0: return LEGAL_RIGGED_DECK
        
        select = obs.get('select', {})
        current = obs.get('current', {})
        p = current.get('players', [{}, {}])[0]
        
        if self.played:
            if select.get('type') not in [0, 1, 9]:
                self.step_tracker += 1
                print(f"\n--- PROMPT {self.step_tracker} ---")
                print(json.dumps(select, indent=2))
                res = super().__call__(obs, config)
                print(f"AGENT CHOSE INDEX {res[0]} -> {json.dumps(select.get('option', [])[res[0]])}")
                return res
            
            if select.get('type') == 0:
                print("\n--- AFTER ENERGY SWITCH (RETURN TO MAIN PHASE) ---")
                print(f"Active ID: {p.get('active', {}).get('id')} Energies: {len(p.get('active', {}).get('energies', []))}")
                for i, b in enumerate(p.get('bench', [])):
                    if b: print(f"Bench {i} ID: {b.get('id')} Energies: {len(b.get('energies', []))}")
                sys.exit(0)
                
        if select.get('type') == 0:
            options = select.get('option', [])
            
            # 1. Try to play Energy Switch first if possible
            for i, opt in enumerate(options):
                hand = p.get('hand', [])
                idx = opt.get('index')
                if idx is not None and idx < len(hand):
                    card = hand[idx]
                    cid = card.get('id') if isinstance(card, dict) else card
                    if cid == 1116: # Energy Switch
                        active_energies = len(p.get('active', {}).get('energies', []))
                        bench_energies = sum(len(b.get('energies', [])) for b in p.get('bench', []) if b)
                        # We need at least 1 energy on the board, and at least 2 pokemon total
                        if (active_energies > 0 or bench_energies > 0) and (p.get('active') and any(p.get('bench', []))):
                            print("\n--- BEFORE ENERGY SWITCH ---")
                            print(f"Active ID: {p.get('active', {}).get('id')} Energies: {active_energies}")
                            for j, b in enumerate(p.get('bench', [])):
                                if b: print(f"Bench {j} ID: {b.get('id')} Energies: {len(b.get('energies', []))}")
                            self.played = True
                            res = super().__call__(obs, config)
                            print(f"AGENT PLAYED INDEX {res[0]} -> {json.dumps(opt)}")
                            return res
                            
            # 2. Otherwise attach energy
            for i, opt in enumerate(options):
                if opt.get('type') == 8: # Energy attach
                    return [i]
                    
            # 3. Otherwise play bench
            for i, opt in enumerate(options):
                if opt.get('type') == 7: # Bench
                    return [i]
                            
        return super().__call__(obs, config)

agent_instance = DumpAgent()
def agent(obs, config): return agent_instance(obs, config)

env = make('cabt', debug=False)
for _ in range(50):
    try: env.run([agent, greedy_agent])
    except SystemExit: break
    except Exception: pass
