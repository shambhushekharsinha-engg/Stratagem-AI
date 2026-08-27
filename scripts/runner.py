import os
from kaggle_environments import make

def random_agent(obs, config):
    import random
    options = obs.get("options", [])
    if not options:
        # Step 0: return deck
        # Build a minimal legal 60-card deck: 4x basic pokemon (id 1), 56x energy (id 2)
        # Using IDs from previous analysis: e.g. some basic pokemon and basic energy
        # Using valid IDs: Basic Pokemon ID 22, Basic Energy ID 1
        deck = [22]*4 + [1]*56
        return deck
    
    # Random valid option
    return [random.randrange(len(options))]

def main():
    print("Initializing CABT environment...")
    env = make("cabt", debug=True)
    
    print("Running match with two random agents...")
    # Play a match
    steps = env.run([random_agent, random_agent])
    
    print(f"Match complete in {len(steps)} steps.")
    
    # Inspect final rewards
    last_step = steps[-1]
    r0 = last_step[0].reward
    r1 = last_step[1].reward
    
    print(f"Agent 0 reward: {r0}")
    print(f"Agent 1 reward: {r1}")
    
    # Check if we can extract data correctly
    if len(steps) > 2:
        obs = steps[2][0].observation
        if 'current' in obs:
            print("Successfully extracted detailed game state from step 2!")
        else:
            print("Warning: 'current' state not found in observation.")

if __name__ == "__main__":
    main()
