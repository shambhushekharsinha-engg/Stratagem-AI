import time
import math
import argparse
import random

from greedy_agent import greedy_agent
from heuristic_agent import agent as heuristic_agent
from midrange_agent import greedy_agent as midrange_agent
from control_agent import greedy_agent as control_agent

try:
    from kaggle_environments import make
except ImportError:
    print("WARNING: kaggle_environments not found. Must run inside Kaggle cabt environment.")
    make = None

def run_match(agents, seed):
    env = make("ptcg", debug=False, configuration={"seed": seed})
    env.run(agents)
    rewards = env.steps[-1][0]['reward'], env.steps[-1][1]['reward']
    # Return 1 if agent 0 wins, 0 if agent 1 wins, 0.5 for tie
    if rewards[0] > rewards[1]: return 1
    if rewards[1] > rewards[0]: return 0
    return 0.5

def calculate_stats(wins, n):
    p = wins / n
    se = math.sqrt(p * (1 - p) / n)
    ci_95 = 1.96 * se
    return p * 100, ci_95 * 100

def batch_simulate(name, agent_test, agent_baseline, n_games, base_seed):
    if make is None: return 0, 0, n_games, 0, 0
    print(f"\n--- Starting {name} ({n_games} games, Seed: {base_seed}) ---")
    
    test_wins = 0
    ties = 0
    
    # 50% games Test vs Baseline (Test is P1)
    half = n_games // 2
    for i in range(half):
        seed = base_seed + i
        random.seed(seed)
        res = run_match([agent_test, agent_baseline], seed)
        if res == 1: test_wins += 1
        elif res == 0.5: ties += 1
        if (i+1) % max(1, (half//5)) == 0:
            print(f"  [P1] Progress: {i+1}/{half} | Test Wins: {test_wins}")
            
    # 50% games Baseline vs Test (Test is P2)
    p2_wins = 0
    for i in range(half, n_games):
        seed = base_seed + i
        random.seed(seed)
        res = run_match([agent_baseline, agent_test], seed)
        if res == 0: 
            test_wins += 1
            p2_wins += 1
        elif res == 0.5: ties += 1
        if (i+1) % max(1, (n_games//5)) == 0:
            print(f"  [P2] Progress: {i+1-half}/{half} | Test Wins as P2: {p2_wins}")
            
    test_wr, ci = calculate_stats(test_wins, n_games)
    print(f"FINAL {name}: Win Rate {test_wr:.1f}% ± {ci:.1f}%")
    return test_wins, n_games - test_wins - ties, ties, test_wr, ci

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--smoke", action="store_true", help="Run a 10-game validation test")
    args = parser.parse_args()
    
    games = 10 if args.smoke else args.games
    print(f"Executing H5 Cross-Archetype Robustness Matrix (N={games}, Seed={args.seed})")
    
    # 1. H1 Aggro Mirror
    w1, l1, t1, wr1, ci1 = batch_simulate('H1_Aggro_Mirror', heuristic_agent, greedy_agent, games, args.seed)
    
    # 2. H5a Evolution/Spread (Dragapult)
    w2, l2, t2, wr2, ci2 = batch_simulate('H5a_Evolution_Spread', heuristic_agent, midrange_agent, games, args.seed + 10000)
    
    # 3. H5b Control/Stall (Slowking)
    w3, l3, t3, wr3, ci3 = batch_simulate('H5b_Control_Stall', heuristic_agent, control_agent, games, args.seed + 20000)
    
    print("\n\n### Generated Markdown Table for PAPER.md ###\n")
    print("| Test | Environment | N | Heuristic WR | Baseline WR | 95% CI | Result |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    if make is not None:
        print(f"| H1 | Aggro Mirror | {games:,} | {wr1:.1f}% | {100-wr1:.1f}% | ±{ci1:.1f}% | {'Heuristic' if wr1>50 else 'Baseline'} Wins |")
        print(f"| H5a | Evolution/Spread | {games:,} | {wr2:.1f}% | {100-wr2:.1f}% | ±{ci2:.1f}% | {'Heuristic' if wr2>50 else 'Baseline'} Wins |")
        print(f"| H5b | Control/Stall | {games:,} | {wr3:.1f}% | {100-wr3:.1f}% | ±{ci3:.1f}% | {'Heuristic' if wr3>50 else 'Baseline'} Wins |")

