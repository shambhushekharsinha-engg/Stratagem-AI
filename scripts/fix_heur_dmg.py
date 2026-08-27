import re

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'r') as f:
    text = f.read()

old_fallback = """            # Attack for max damage
            max_dmg = -1
            best_atk = None
            for i, opt in enumerate(options):
                if is_attack_option(opt):
                    dmg = calculate_projected_damage(opt, my_active, opp_active)
                    if dmg > max_dmg:
                        max_dmg = dmg
                        best_atk = i
            if best_atk is not None:
                return best_atk
            return None"""

new_fallback = """            # Attack for max damage
            max_atk_id = -1
            best_atk = None
            for i, opt in enumerate(options):
                if is_attack_option(opt):
                    atk_id = opt.get('attackId', 0)
                    if atk_id > max_atk_id:
                        max_atk_id = atk_id
                        best_atk = i
            if best_atk is not None:
                return best_atk
            return None"""

text = text.replace(old_fallback, new_fallback)

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'w') as f:
    f.write(text)
