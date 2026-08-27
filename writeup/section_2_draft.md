# §2 Game Mechanics Analysis (~165 words)

Pokémon TCG is a stochastic, partial-information extensive-form game. Unlike chess or Go, the full game state is never visible — each player sees only their own hand, their prize stack, and the shared public board (active Pokémon, bench, attachments, discard). The opponent's hand and deck order remain hidden throughout.

This hidden information forces effective agents away from deterministic search toward probabilistic inference: tracking which cards the opponent has played narrows the distribution of remaining options, making responses like holding a disruption Supporter more or less likely.

The decision space is deceptively large. A single turn can chain draw Supporters (expanding the hand mid-turn), search Trainers, energy attachments, and abilities before resolving an attack — creating branching sequences that pure heuristics struggle to evaluate accurately.

Above all, PTCG is a race. Six prizes are taken by dealing KOs; there is no sustained healing mechanic to reset momentum. This motivates the hypothesis — tested in §5 (H2) — that tempo dominates outcomes: the agent that takes the first prize and sustains pressure should win most games. §4's priority stack assumes this; §5 tests it.
