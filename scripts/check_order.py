import os, sys, time
from multiprocessing import Pool

def worker(seed):
    sys.path.append('C:\\Stratagem-AI')
    from kaggle_environments import make
    from heuristic_agent import HeuristicAgent
    from greedy_agent import greedy_agent
    env = make('cabt', debug=False)
    agent1 = HeuristicAgent()
    agent2 = greedy_agent
    if seed % 2 == 0:
        env.run([agent1, agent2])
        r = env.steps[-1][0]['reward']
        return ('first', 1 if r == 1 else 0)
    else:
        env.run([agent2, agent1])
        r = env.steps[-1][1]['reward']
        return ('second', 1 if r == 1 else 0)

if __name__ == '__main__':
    with Pool(os.cpu_count()) as p:
        results = p.map(worker, range(100))
    first_wins = sum(1 for r in results if r[0] == 'first' and r[1] == 1)
    second_wins = sum(1 for r in results if r[0] == 'second' and r[1] == 1)
    print(f'First Wins: {first_wins}/50')
    print(f'Second Wins: {second_wins}/50')
