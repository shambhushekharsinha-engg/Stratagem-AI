import re

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'r') as f:
    text = f.read()

# Fix the broken replacement
bad_block = """                            self.pending_action = None
        self.gust_count = 0
        self.retreat_count = 0
                            return [i]"""
good_block = """                            self.pending_action = None
                            return [i]"""
text = text.replace(bad_block, good_block)

# Add the counters to the correct place (__init__)
bad_init = """    def __init__(self):
        self.pending_action = None # Dict holding context: {'type': 'GUST', 'target': b_mon}"""
good_init = """    def __init__(self):
        self.pending_action = None # Dict holding context: {'type': 'GUST', 'target': b_mon}
        self.gust_count = 0
        self.retreat_count = 0"""
text = text.replace(bad_init, good_init)

with open('C:\\Stratagem-AI\\heuristic_agent.py', 'w') as f:
    f.write(text)
