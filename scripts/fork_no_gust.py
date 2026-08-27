import re

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'r') as f:
    text = f.read()

# Strip out Priority 2 entirely for the H3 A/B test
text = text.replace('if gust is not None:\n            self.gust_count += 1\n            return [gust]', '# No Gust Priority (H3 A/B Arm)')

with open('C:\\Stratagem-AI\\heuristic_agent_no_gust.py', 'w') as f:
    f.write(text)
