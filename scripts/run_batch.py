import os
import sys
from multiprocessing import Pool
import time

def worker(seed):
    sys.path.append('C:\\Stratagem-AI')
    from kaggle_environments import make
    from heuristic_agent import HeuristicAgent
    from greedy_agent import greedy_agent
    
    env = make("cabt", debug=False)
    agent1 = HeuristicAgent()
    agent2 = greedy_agent
    
    try:
        if seed % 2 == 0:
            env.run([agent1, agent2])
            r1, r2 = env.steps[-1][0]['reward'], env.steps[-1][1]['reward']
            return (1 if r1 == 1 else (0 if r2 == 1 else 0.5))
        else:
            env.run([agent2, agent1])
            r1, r2 = env.steps[-1][1]['reward'], env.steps[-1][0]['reward']
            return (1 if r1 == 1 else (0 if r2 == 1 else 0.5))
    except Exception as e:
        return None

if __name__ == '__main__':
    num_games = 1000
    print(f"Starting {num_games} matches...")
    start_time = time.time()
    
    # Remove old trace if exists
    if os.path.exists('C:\\Stratagem-AI\\eswitch_live_trace.jsonl'):
        os.remove('C:\\Stratagem-AI\\eswitch_live_trace.jsonl')
        
    with Pool(os.cpu_count()) as p:
        results = p.map(worker, range(num_games))
        
    wins = sum(1 for r in results if r == 1)
    losses = sum(1 for r in results if r == 0)
    ties = sum(1 for r in results if r == 0.5)
    errors = sum(1 for r in results if r is None)
    
    print(f"\n--- BATCH COMPLETE ---")
    print(f"Total Games: {num_games}")
    print(f"Wins: {wins}")
    print(f"Losses: {losses}")
    print(f"Ties: {ties}")
    print(f"Errors: {errors}")
    win_rate = wins / max(1, (wins + losses))
    print(f"Win Rate (excluding errors/ties): {win_rate:.2%}")
    print(f"Time taken: {time.time() - start_time:.2f} seconds")
