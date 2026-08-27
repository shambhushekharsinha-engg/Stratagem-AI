import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

directory = r'C:\Stratagem-AI\data\episodes'
files = [f for f in os.listdir(directory) if f.endswith('.json')]

print(f"Scanning {len(files)} episodes for edge cases...")

lengths = {}
reward_pairs = Counter()
status_pairs = Counter()

error_episode = None
tie_episode = None
shortest_episode = None
min_len = float('inf')
max_len = 0
longest_episode = None

for f_name in files:
    path = os.path.join(directory, f_name)
    with open(path, encoding='utf-8') as f:
        try:
            data = json.load(f)
        except:
            continue
            
    steps = data.get('steps', [])
    n_steps = len(steps)
    
    if n_steps < min_len:
        min_len = n_steps
        shortest_episode = f_name
    if n_steps > max_len:
        max_len = n_steps
        longest_episode = f_name
        
    if n_steps > 0:
        last_step = steps[-1]
        r0 = last_step[0].get('reward')
        r1 = last_step[1].get('reward')
        s0 = last_step[0].get('status')
        s1 = last_step[1].get('status')
        
        reward_pairs[(r0, r1)] += 1
        status_pairs[(s0, s1)] += 1
        
        if r0 == 0 and r1 == 0 and tie_episode is None:
            tie_episode = f_name
        if (s0 == 'ERROR' or s1 == 'ERROR') and error_episode is None:
            error_episode = f_name

print(f"\nScan complete.")
print(f"Min steps: {min_len} ({shortest_episode})")
print(f"Max steps: {max_len} ({longest_episode})")

print("\nObserved Final Reward Pairs (P0, P1):")
for pair, count in reward_pairs.items():
    print(f"  {pair}: {count} episodes")
    
print("\nObserved Final Status Pairs (P0, P1):")
for pair, count in status_pairs.items():
    print(f"  {pair}: {count} episodes")

if error_episode:
    print(f"\nFound an ERROR episode: {error_episode}")
    with open(os.path.join(directory, error_episode), encoding='utf-8') as f:
        err_data = json.load(f)
        print(f"  Error step count: {len(err_data['steps'])}")
        if len(err_data['steps']) > 0:
            print(f"  Last step info:")
            print(f"    P0 Status: {err_data['steps'][-1][0].get('status')}, Reward: {err_data['steps'][-1][0].get('reward')}")
            print(f"    P1 Status: {err_data['steps'][-1][1].get('status')}, Reward: {err_data['steps'][-1][1].get('reward')}")
