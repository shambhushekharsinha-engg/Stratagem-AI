with open('C:\\Stratagem-AI\\heuristic_agent.py', 'r') as f:
    text = f.read()

text = text.replace('return best_opt', 'if best_opt is not None: print(f"\\n--- FIRE: find_gust_ko chosen! Option {best_opt} ---\\n")\n            return best_opt')
text = text.replace('return best_retreat_opt', 'if best_retreat_opt is not None: print(f"\\n--- FIRE: find_safe_retreat chosen! Option {best_retreat_opt} ---\\n")\n            return best_retreat_opt')

with open('C:\\Stratagem-AI\\heuristic_agent_logged.py', 'w') as f:
    f.write(text)
