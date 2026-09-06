import os

with open("reproduce/heuristic_agent.py", "r", encoding="utf-8") as f:
    heur = f.read()

header = """import time
import multiprocessing
import random

# ----------------- GREEDY AGENT -----------------
def greedy_agent(obs, config):
    if obs.step == 0:
        return ([96]*4 + [916]*4 + [1]*12 + [1182]*4 + [1213]*4 + [1192]*4 + [1191]*4 + [1086]*4 + [1121]*4 + [1123]*4 + [1116]*4 + [1077]*4 + [1083]*4)
    select = obs.get('select', {})
    options = obs.get('options', [])
    min_req = select.get('minCount', 1)
    if not options: return list(range(min_req))
    def is_attack_option(opt):
        return isinstance(opt, dict) and 'attackId' in opt
    attack_options = [(idx, opt) for idx, opt in enumerate(options) if is_attack_option(opt)]
    if attack_options:
        scored_opts = []
        for idx, opt in attack_options:
            attack_idx = opt.get('attackId', 0)
            score = attack_idx * 10
            scored_opts.append((score, idx))
        scored_opts.sort(key=lambda x: x[0], reverse=True)
        return [idx for score, idx in scored_opts[:min_req]]
    scored_opts = []
    for idx, opt in enumerate(options):
        score = 0
        if isinstance(opt, dict):
            if 'active' in opt: score -= 5
            if 'bench' in opt: score += 5
            if opt.get('type') == 'Boss''s Orders': score += 20
            if 'Trainer' in str(opt): score += 10
            if 'Energy' in str(opt): score += 15
        scored_opts.append((score, idx))
    scored_opts.sort(key=lambda x: x[0], reverse=True)
    if scored_opts: return [idx for score, idx in scored_opts[:min_req]]
    return list(range(min(min_req, len(options))))

# ----------------- MIDRANGE AGENT -----------------
def midrange_agent(obs, config):
    if obs.step == 0:
        return ([119]*4 + [120]*4 + [121]*4 + [2]*6 + [5]*6 + [1182]*4 + [1213]*4 + [1192]*4 + [1191]*4 + [1086]*4 + [1121]*4 + [1123]*4 + [1116]*4 + [1077]*4)
    return greedy_agent(obs, config)

# ----------------- CONTROL AGENT -----------------
def control_agent(obs, config):
    if obs.step == 0:
        return ([162]*4 + [163]*4 + [7]*12 + [1182]*4 + [1213]*4 + [1192]*4 + [1191]*4 + [1086]*4 + [1121]*4 + [1123]*4 + [1116]*4 + [1077]*4 + [1083]*4)
    return greedy_agent(obs, config)

# ----------------- HEURISTIC AGENT -----------------
"""

footer = """
heuristic_agent = agent

try:
    from kaggle_environments import make
except ImportError:
    print("WARNING: kaggle_environments not found.")
    make = None

def run_match(agents):
    env = make("ptcg", debug=False)
    env.run(agents)
    r = env.steps[-1][0]['reward'], env.steps[-1][1]['reward']
    return 1 if r[0] > r[1] else (0 if r[1] > r[0] else -1)

def batch_simulate(name, agent1, agent2, n_games=1000):
    if make is None: return
    print(f"Starting {name} for {n_games} games...")
    wins, losses, ties = 0, 0, 0
    for i in range(n_games):
        res = run_match([agent1, agent2])
        if res == 1: wins += 1
        elif res == 0: losses += 1
        else: ties += 1
        if i > 0 and i % 50 == 0: print(f"{name} Progress: {i}/{n_games} | Wins: {wins} | Losses: {losses} | Ties: {ties}")
    print(f"FINAL {name}: Wins: {wins} | Losses: {losses} | Ties: {ties}")

if __name__ == '__main__':
    batch_simulate('Heuristic_vs_Midrange', heuristic_agent, midrange_agent, 1000)
    batch_simulate('Heuristic_vs_Control', heuristic_agent, control_agent, 1000)
"""

with open("kaggle_kernel/runner.py", "w", encoding="utf-8") as f:
    f.write(header + heur + footer)
