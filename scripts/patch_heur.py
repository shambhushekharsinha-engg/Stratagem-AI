with open('heuristic_agent.py', 'r') as f:
    text = f.read()

text = text.replace('return best_opt', 'print("\\n--- FIRE: find_gust_ko chosen! ---"); return best_opt')
text = text.replace('return best_retreat_opt', 'print("\\n--- FIRE: find_safe_retreat chosen! ---"); return best_retreat_opt')

with open('heuristic_agent_logged.py', 'w') as f:
    f.write(text)
