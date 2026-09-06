import os, sys, json
from kaggle_environments import make

sys.path.append('C:\\Stratagem-AI')
from heuristic_agent import HeuristicAgent
from greedy_agent import greedy_agent

env = make('cabt', debug=False)
agent1 = HeuristicAgent()
agent2 = greedy_agent

losses = []
step_counts = []

for i in range(10):
    env.run([agent1, agent2])
    r1 = env.steps[-1][0]['reward']
    step_counts.append(len(env.steps))
    if r1 != 1 and len(losses) < 3:
        losses.append(env.steps)
        
print(f'Step counts for 10 games: {step_counts}')

if losses:
    loss = losses[0]
    print(f'\n--- ANALYZING LOSS 1 (Length: {len(loss)} steps) ---')
    for i in range(max(0, len(loss)-10), len(loss)):
        step = loss[i]
        obs = step[0]['observation']
        print(f'Step {i}:')
        if 'select' in obs:
            print(f'  Select Type: {obs["select"].get("type")}')
        print(f'  Action P1: {step[0].get("action")}')
        print(f'  Action P2: {step[1].get("action")}')
        print(f'  Reward P1: {step[0].get("reward")}')
        
    with open('loss_1_full.json', 'w') as f:
        json.dump(loss, f, indent=2)
