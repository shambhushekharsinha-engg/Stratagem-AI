import re

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'r') as f:
    text = f.read()

# Fix find_lethal_ko
old_lethal = """                    for b_mon in opp_state.get('bench', []):
                        if not b_mon: continue
                        prizes_taken = 2 if b_mon.get('is_ex') else 1
                        if prizes_taken >= my_prizes:
                            for atk in affordable:
                                if b_mon.get('hp', 0) - b_mon.get('damage', 0) <= calculate_projected_damage(atk, my_active, b_mon):
                                    self.pending_action = {'type': 'GUST', 'target': b_mon}
                                    return i"""
new_lethal = """                    for b_idx, b_mon in enumerate(opp_state.get('bench', [])):
                        if not b_mon: continue
                        prizes_taken = 2 if b_mon.get('is_ex') else 1
                        if prizes_taken >= my_prizes:
                            for atk in affordable:
                                if b_mon.get('hp', 0) - b_mon.get('damage', 0) <= calculate_projected_damage(atk, my_active, b_mon):
                                    self.pending_action = {'type': 'GUST', 'target_idx': b_idx}
                                    return i"""
text = text.replace(old_lethal, new_lethal)

# Fix find_gust_ko
old_gust = """                    for b_mon in opp_state.get('bench', []):
                        if not b_mon: continue
                        for atk in affordable:
                            if b_mon.get('hp', 0) - b_mon.get('damage', 0) <= calculate_projected_damage(atk, my_active, b_mon):
                                self.pending_action = {'type': 'GUST', 'target': b_mon}
                                return i"""
new_gust = """                    for b_idx, b_mon in enumerate(opp_state.get('bench', [])):
                        if not b_mon: continue
                        for atk in affordable:
                            if b_mon.get('hp', 0) - b_mon.get('damage', 0) <= calculate_projected_damage(atk, my_active, b_mon):
                                self.pending_action = {'type': 'GUST', 'target_idx': b_idx}
                                return i"""
text = text.replace(old_gust, new_gust)

# Fix Multi-Step Target Resolution
old_resolve = """                if action_type == 'GUST':
                    target = self.pending_action.get('target')
                    for i, opt in enumerate(options):
                        if opt.get('index') == target.get('index'):
                            self.pending_action = None
                            return [i]"""
new_resolve = """                if action_type == 'GUST':
                    target_idx = self.pending_action.get('target_idx')
                    for i, opt in enumerate(options):
                        if opt.get('index') == target_idx:
                            self.pending_action = None
                            return [i]
                    self.pending_action = None # Clear if not found to avoid lock"""
text = text.replace(old_resolve, new_resolve)

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'w') as f:
    f.write(text)
