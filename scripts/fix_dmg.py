import re

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'r') as f:
    text = f.read()

old_calc = """        def calculate_projected_damage(atk_opt, attacker, target_mon):
            base_dmg = atk_opt.get('damage', 0)
            if not target_mon or not attacker: return 0
            my_type = attacker.get('type')
            weakness = target_mon.get('weakness')
            resistance = target_mon.get('resistance')
            final_dmg = base_dmg
            if weakness and weakness == my_type: final_dmg *= 2
            if resistance and resistance == my_type: final_dmg -= 30
            return max(0, final_dmg)"""

new_calc = """        def calculate_projected_damage(atk_opt, attacker, target_mon):
            if not target_mon or not attacker: return 0
            base_dmg = get_opp_max_dmg(attacker)
            my_type = attacker.get('type')
            weakness = target_mon.get('weakness')
            resistance = target_mon.get('resistance')
            final_dmg = base_dmg
            if weakness and weakness == my_type: final_dmg *= 2
            if resistance and resistance == my_type: final_dmg -= 30
            return max(0, final_dmg)"""

text = text.replace(old_calc, new_calc)

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'w') as f:
    f.write(text)
