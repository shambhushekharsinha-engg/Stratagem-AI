with open('C:\\Stratagem-AI\\heuristic_agent.py', 'r') as f:
    text = f.read()

# Fix the bad replacement everywhere
bad_str = "self.pending_action = None\n        self.gust_count = 0\n        self.retreat_count = 0"
text = text.replace(bad_str, "self.pending_action = None")

# Now selectively add to __init__
good_init = """    def __init__(self):
        self.pending_action = None # Dict holding context: {'type': 'GUST', 'target': b_mon}
        self.gust_count = 0
        self.retreat_count = 0"""
text = text.replace("    def __init__(self):\n        self.pending_action = None # Dict holding context: {'type': 'GUST', 'target': b_mon}", good_init)

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'w') as f:
    f.write(text)
