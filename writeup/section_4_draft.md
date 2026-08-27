# §4 Agent Architecture and Priority Stack

The agent operates on a deterministic, heuristic-driven priority stack rather than deep search algorithms like MCTS or reinforcement learning. Because the game involves high variance and hidden information, forward-searching probability trees is computationally expensive and prone to error. Instead, the agent leverages the linear deck described in §3 to execute a hierarchical set of rules, evaluating the board state each turn and taking the highest-priority legal action.

**Setup and Resource Phase**
During the early game, the agent prioritizes board development and deck thinning. The heuristic greedily exhausts unconditional draw Supporters and targeted search Items to deploy primary Basic attackers and secure Energy. Because the deck omits situational tech cards, the agent does not need to calculate long-term hold-value for its hand; it plays resources immediately to establish tempo. Energy attachments default to the Active Pokémon until its attack cost is met, after which the agent accelerates remaining Energy to the Bench.

**The Combat Priority Stack**
Once combat begins, the agent shifts to a strict evaluation hierarchy designed to press the prize race (H2). Before declaring an attack, the agent evaluates the board and acts in this exact sequence:
1. **Lethal:** If an action sequence secures the final prize card, execute it immediately.
2. **Targeted KO (Gusting):** If the opponent’s Active Pokémon cannot be knocked out, but a Benched Pokémon can, use a gusting effect to pull the weaker target forward and secure a prize. The expected value of this decision is evaluated in §5 (H3).
3. **Active KO:** If gusting is unavailable, execute the attack required to knock out the Active Pokémon.
4. **Retreat and Preserve:** If no immediate KO is possible, evaluate defensive positioning. If the Active Pokémon is within lethal range of the opponent's board and a powered Benched attacker is ready, retreat to deny the opponent a prize.
5. **Damage Maximization:** If retreating is unnecessary or impossible, execute the attack that yields the highest raw damage, provided it does not discard irreplaceable Energy.

**Information Management**
To handle hidden information efficiently, the agent uses a simplified worst-case model. Rather than calculating exact probabilities of the opponent's hand, it assumes the opponent will always take a prize card next turn if mathematically possible on the public board. This forces the agent to prioritize immediate aggression over slow setup, perfectly mirroring the deck's philosophy. This deterministic, highly linear framework guarantees consistent play, producing the reliable baseline required for the empirical tests in §5.
