import json
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Find first json
directory = r'C:\Stratagem-AI\data\episodes'
files = [f for f in os.listdir(directory) if f.endswith('.json')]
if not files:
    print("No JSON files found!")
    sys.exit(1)

first_file = os.path.join(directory, files[0])
print(f'Inspecting {first_file} ({os.path.getsize(first_file)} bytes)')

with open(first_file, encoding='utf-8') as f:
    data = json.load(f)

print('\nTop-level keys:', list(data.keys()))

print('\nInfo (metadata):')
for k, v in data.get('info', {}).items():
    print(f'  {k}: {v}')

steps = data.get('steps', [])
print(f'\nTotal steps: {len(steps)}')

if steps:
    step0 = steps[0]
    print('\nStep 0 (First Step):')
    if isinstance(step0, list):
        for i, agent in enumerate(step0):
            print(f'  Agent {i} Keys: {list(agent.keys())}')
            print(f'  Agent {i} Status: {agent.get("status")}')
            print(f'  Agent {i} Action Type: {type(agent.get("action"))}')
            if isinstance(agent.get('action'), list):
                 print(f'  Agent {i} Action Length: {len(agent.get("action"))}')
                 print(f'  Agent {i} Action Sample: {agent.get("action")[:5]}')
            
            obs = agent.get('observation', {})
            print(f'  Agent {i} Observation Keys: {list(obs.keys())}')
            
            # Print select format if available
            select = obs.get('select')
            if select:
                 print(f'  Agent {i} Select format: {list(select.keys())}')
            else:
                 print(f'  Agent {i} Select is None')
            
            # Check what's in logs or current
            current = obs.get('current', {})
            if current:
                 print(f'  Agent {i} Current Keys: {list(current.keys())}')

    last_step = steps[-1]
    print('\nLast step format:')
    if isinstance(last_step, list):
        for i, agent in enumerate(last_step):
            print(f'  Agent {i} Status: {agent.get("status")}')
            print(f'  Agent {i} Reward: {agent.get("reward")}')
