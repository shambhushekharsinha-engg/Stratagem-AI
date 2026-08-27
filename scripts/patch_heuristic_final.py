import re

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'r') as f:
    text = f.read()

# Fix is_play_boss IDs
text = re.sub(r'card_id in \[1077,\s*1111\]', 'card_id in [1182, 1088, 1124]', text)

# Add counters to __init__
if 'self.gust_count' not in text:
    text = text.replace('self.pending_action = None', 'self.pending_action = None\n        self.gust_count = 0\n        self.retreat_count = 0')

# Increment gust counter
if 'self.gust_count += 1' not in text:
    text = text.replace('if gust is not None: return [gust]', 'if gust is not None:\n            self.gust_count += 1\n            return [gust]')

# Increment retreat counter
if 'self.retreat_count += 1' not in text:
    text = text.replace('if retreat is not None: return [retreat]', 'if retreat is not None:\n            self.retreat_count += 1\n            return [retreat]')

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'w') as f:
    f.write(text)
