import time
import multiprocessing

# Note: This runner must be executed in an environment where the 'cabt' engine is available
# (e.g. the Kaggle PTCG python environment).

from greedy_agent import greedy_agent
from heuristic_agent import heuristic_agent
from midrange_agent import midrange_agent
from control_agent import control_agent

# Mock import for the Kaggle environment
try:
    from kaggle_environments import make
except ImportError:
    print("WARNING: kaggle_environments not found. This script must be run where the cabt engine is installed.")
    make = None

def run_match(agents):
    env = make("ptcg", debug=False)
    # The first agent is index 0, second is index 1.
    env.run(agents)
    rewards = env.steps[-1][0]['reward'], env.steps[-1][1]['reward']
    return 1 if rewards[0] > rewards[1] else (0 if rewards[1] > rewards[0] else -1)

def batch_simulate(agent1, agent2, n_games=1000):
    if make is None:
        return 0, 0
    print(f"Starting {n_games} games...")
    wins = 0
    losses = 0
    ties = 0
    
    # Run sequentially for safety if multiprocessing fails with cabt C++ engine,
    # but ideally use multiprocessing in a real Kaggle notebook.
    for i in range(n_games):
        res = run_match([agent1, agent2])
        if res == 1: wins += 1
        elif res == 0: losses += 1
        else: ties += 1
        if i % 100 == 0: print(f"Progress: {i}/{n_games} | Wins: {wins} | Losses: {losses}")
        
    return wins, losses

if __name__ == "__main__":
    print("--- P0 Robustness Matrix Execution ---")
    
    # 1. Aggro Mirror (Baseline)
    print("\nScenario 1: Heuristic (Aggro) vs Greedy (Aggro)")
    # w, l = batch_simulate(heuristic_agent, greedy_agent, 1000)
    print("Expected from previous runs: ~409 Wins (40.9%)")
    
    # 2. Heuristic vs Midrange
    print("\nScenario 2: Heuristic (Aggro) vs Greedy (Midrange/Dragapult ex)")
    # w, l = batch_simulate(heuristic_agent, midrange_agent, 1000)
    
    # 3. Heuristic vs Control
    print("\nScenario 3: Heuristic (Aggro) vs Greedy (Control/Slowking)")
    # w, l = batch_simulate(heuristic_agent, control_agent, 1000)
    
    print("\nRun these functions in your Kaggle notebook to get the true empirical win rates for the matrix!")
