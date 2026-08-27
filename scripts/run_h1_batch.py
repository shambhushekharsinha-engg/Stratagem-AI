import multiprocessing
import sys
sys.path.append('C:\\Stratagem-AI')
from kaggle_environments import make
from greedy_agent import greedy_agent

def run_game(args):
    idx, p0_is_heur = args
    env = make('cabt', debug=False)
    
    # Import locally for multiprocessing
    from heuristic_agent import HeuristicAgent
    agent_heur = HeuristicAgent()
    
    agent0 = agent_heur if p0_is_heur else greedy_agent
    agent1 = greedy_agent if p0_is_heur else agent_heur
    
    env.run([agent0, agent1])
    
    p0_reward = env.steps[-1][0]['reward']
    
    # We can access the instance variables!
    gusts = agent_heur.gust_count
    retreats = agent_heur.retreat_count
    
    return (idx, p0_is_heur, p0_reward, gusts, retreats)

if __name__ == '__main__':
    games = [(i, i % 2 == 0) for i in range(1000)]
    
    print("Starting H1 1000-game batch...")
    with multiprocessing.Pool() as pool:
        results = pool.map(run_game, games)
    
    heur_wins = 0
    total_gusts = 0
    total_retreats = 0
    
    for idx, p0_is_heur, p0_reward, gusts, retreats in results:
        if p0_is_heur and p0_reward == 1: heur_wins += 1
        elif not p0_is_heur and p0_reward == -1: heur_wins += 1
        
        total_gusts += gusts
        total_retreats += retreats
        
    print(f'\\nH1 RESULTS (1000 games):')
    print(f'Heuristic Wins: {heur_wins}/1000 ({heur_wins/10}% win rate)')
    print(f'Total Gusts Fired: {total_gusts}')
    print(f'Total Retreats Fired: {total_retreats}')
