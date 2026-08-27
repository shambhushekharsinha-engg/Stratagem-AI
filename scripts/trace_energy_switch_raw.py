import json
import sys
from kaggle_environments import make

sys.path.append('C:\\Stratagem-AI')
from heuristic_agent import HeuristicAgent
from greedy_agent import greedy_agent

RIGGED_DECK = [96]*15 + [916]*15 + [1]*15 + [1116]*15

class DumpAgent(HeuristicAgent):
    def __init__(self):
        super().__init__()
        self.played = False

    def __call__(self, obs, config):
        if obs.step == 0: return RIGGED_DECK
        
        select = obs.get('select', {})
        current = obs.get('current', {})
        p = current.get('players', [{}, {}])[0]
        
        if self.played:
            print(f"STEP {obs.step} - SELECT PROMPT:\n{json.dumps(select, indent=2)}")
            # After printing the follow up prompt, we can exit or just let it crash
            
            if select.get('type') == 0:
                print("--- RETURNED TO MAIN PHASE ---")
                print(f"Active Energies: {len(p.get('active', {}).get('energies', []))}")
                for i, b in enumerate(p.get('bench', [])):
                    if b: print(f"Bench {i} Energies: {len(b.get('energies', []))}")
                sys.exit(0)
                
            res = super().__call__(obs, config)
            print(f"AGENT CHOSE INDEX {res[0]} -> {json.dumps(select.get('option', [])[res[0]])}")
            return res
            
        if select.get('type') == 0:
            options = select.get('option', [])
            for i, opt in enumerate(options):
                if opt.get('type') == 8: # Energy attach
                    return [i]
                    
            for i, opt in enumerate(options):
                if opt.get('type') == 7: # Bench
                    return [i]
                    
            for i, opt in enumerate(options):
                hand = p.get('hand', [])
                idx = opt.get('index')
                if idx is not None and idx < len(hand):
                    card = hand[idx]
                    cid = card.get('id') if isinstance(card, dict) else card
                    if cid == 1116: # Energy Switch
                        # Do we have energy somewhere?
                        active_energies = len(p.get('active', {}).get('energies', []))
                        bench_energies = sum(len(b.get('energies', [])) for b in p.get('bench', []) if b)
                        if active_energies > 0 or bench_energies > 0:
                            print("\n--- PLAYING ENERGY SWITCH ---")
                            print(f"Active Energies BEFORE: {active_energies}")
                            for j, b in enumerate(p.get('bench', [])):
                                if b: print(f"Bench {j} Energies BEFORE: {len(b.get('energies', []))}")
                            self.played = True
                            return [i]
                            
        return super().__call__(obs, config)

agent_instance = DumpAgent()
def agent(obs, config): return agent_instance(obs, config)

env = make('cabt', debug=False)
for _ in range(50):
    try: env.run([agent, greedy_agent])
    except SystemExit: break
    except Exception: pass
