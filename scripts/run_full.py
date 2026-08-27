
import os, sys, time
from multiprocessing import Pool
from kaggle_environments import make

def worker(seed):
    sys.path.append('C:\\\\Stratagem-AI')
    from heuristic_agent import HeuristicAgent
    from greedy_agent import greedy_agent
    env = make('cabt', debug=False)
    agent1 = HeuristicAgent()
    agent2 = greedy_agent
    if seed % 2 == 0:
        env.run([agent1, agent2])
        status = env.steps[-1][0]['status']
        r = env.steps[-1][0]['reward']
        return ('first', 1 if r == 1 else 0, status)
    else:
        env.run([agent2, agent1])
        status = env.steps[-1][1]['status']
        r = env.steps[-1][1]['reward']
        return ('second', 1 if r == 1 else 0, status)

if __name__ == '__main__':
    start = time.time()
    with Pool(os.cpu_count()) as p:
        results = p.map(worker, range(1000))
    first_wins = sum(1 for r in results if r[0] == 'first' and r[1] == 1)
    second_wins = sum(1 for r in results if r[0] == 'second' and r[1] == 1)
    errors = sum(1 for r in results if r[2] in ['ERROR', 'INVALID'])
    
    print(f'Runtime: {time.time()-start:.2f}s')
    print(f'Errors/Invalids: {errors}')
    print(f'First Wins (Agent as P0): {first_wins}/500')
    print(f'Second Wins (Agent as P1): {second_wins}/500')
    print(f'Total Win Rate: {(first_wins+second_wins)/10}%')
