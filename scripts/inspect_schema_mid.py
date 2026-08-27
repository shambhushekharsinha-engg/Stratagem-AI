import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Stratagem-AI\data\episodes\93459262.json', encoding='utf-8') as f:
    data = json.load(f)

steps = data.get('steps', [])
if len(steps) > 20:
    step_mid = steps[20]
    obs = step_mid[0].get('observation', {})
    current = obs.get('current', {})

    print('Step 20 - Mid Game observation:')
    p0 = current['players'][0]
    print(f"Player 0 active: {p0.get('active')}")
    print(f"Player 0 bench: {p0.get('bench')}")
    print(f"Player 0 hand: {p0.get('hand')}")
    print(f"Player 0 prize: {p0.get('prize')}")
    print(f"Player 0 discard length: {len(p0.get('discard', []))}")

    print('\nLog snippet from Step 20:')
    logs = obs.get('logs', [])
    for log in logs[:10]:
         print(f"  {log}")

if len(steps) > 0:
    print("\nLooking at the end of the game to see final prizes:")
    last_step = steps[-2]
    obs_last = last_step[0].get('observation', {})
    cur_last = obs_last.get('current', {})
    if cur_last:
        p0_last = cur_last['players'][0]
        p1_last = cur_last['players'][1]
        print(f"Player 0 final prizes: {len(p0_last.get('prize', []))}")
        print(f"Player 1 final prizes: {len(p1_last.get('prize', []))}")
        print(f"Game result: {cur_last.get('result')}")
