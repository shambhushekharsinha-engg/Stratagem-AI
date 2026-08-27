import json
import os

with open(r'C:\Stratagem-AI\data\episodes\93459262.json', encoding='utf-8') as f:
    data = json.load(f)

steps = data.get('steps', [])

print("Step 1 (Agent actions for deck selection):")
step1 = steps[1]
for i, agent in enumerate(step1):
    action = agent.get('action', [])
    print(f"  Agent {i} Action Type: {type(action)}")
    print(f"  Agent {i} Action Length: {len(action) if isinstance(action, list) else 'N/A'}")
    if isinstance(action, list):
         print(f"  Agent {i} Deck snippet: {action[:10]}")

print("\nObservation keys and details in Step 1:")
obs = step1[0].get('observation', {})
current = obs.get('current', {})
print(f"  Current Keys: {list(current.keys())}")
if current:
    print(f"    players: {len(current.get('players', []))}")
    print(f"    turn: {current.get('turn')}")
    print(f"    result: {current.get('result')}")
    print(f"    yourIndex: {current.get('yourIndex')}")
    p0 = current['players'][0]
    print(f"    Player 0 Keys: {list(p0.keys())}")
    print(f"    Player 0 active: {p0.get('active')}")
    print(f"    Player 0 bench: {len(p0.get('bench', []))}")
    print(f"    Player 0 prize: {p0.get('prize')}")
    print(f"    Player 0 hand (count?): {len(p0.get('hand', [])) if isinstance(p0.get('hand'), list) else p0.get('hand')}")
    
print("\nLog snippet from Step 1:")
logs = obs.get('logs', [])
print(f"  Total logs in step 1: {len(logs)}")
for i, log in enumerate(logs[:5]):
    print(f"    Log {i}: {log}")
