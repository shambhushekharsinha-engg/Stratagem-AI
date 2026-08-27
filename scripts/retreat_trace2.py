import sys
sys.path.append('C:\\Stratagem-AI')
from kaggle_environments import make
from heuristic_agent import HeuristicAgent
from greedy_agent import greedy_agent

class TracedAgent(HeuristicAgent):
    def __call__(self, obs, config):
        res = super().__call__(obs, config)
        if hasattr(self, 'retreat_count') and self.retreat_count > getattr(self, '_last_rc', 0):
            self._last_rc = self.retreat_count
            print("\\n--- RETREAT TRIGGERED ---", file=sys.stderr)
            my_state = obs.current.get('players')[obs.current.get('yourIndex')]
            opp_state = obs.current.get('players')[1 - obs.current.get('yourIndex')]
            print(f"My Active: {my_state.get('active')}", file=sys.stderr)
            print(f"Opp Active: {opp_state.get('active')}", file=sys.stderr)
            print(f"My Bench: {my_state.get('bench')}", file=sys.stderr)
            
            with open('C:\\Stratagem-AI\\retreat_log.txt', 'w') as f:
                f.write("RETREAT TRIGGERED\\n")
                f.write(f"My Active: {my_state.get('active')}\\n")
                f.write(f"Opp Active: {opp_state.get('active')}\\n")
                f.write(f"My Bench: {my_state.get('bench')}\\n")
            raise RuntimeError("STOP")
        return res

env = make('cabt', debug=False)
for i in range(100):
    try:
        env.run([TracedAgent(), greedy_agent])
    except RuntimeError:
        print("Found retreat!")
        sys.exit(0)
