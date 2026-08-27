# §3 Deck Construction Strategy

Out of the 1,267 unique cards in the expanded pool, the deck was built to minimize the agent's decision-making complexity while maximizing tempo.

**Archetype and Consistency**
We selected a fast, aggressive archetype focused exclusively on high-HP Basic attackers. Evolving Stage 1 and 2 Pokémon introduces variance—requiring specific pieces over multiple turns—and demands complex sequencing. Heavy-hitting Basic Pokémon ensure immediate pressure from turn one, executing the tempo advantage discussed in §2.

To support this, the Trainer lineup runs maximum copies of unconditional draw Supporters and targeted search Items, avoiding situational tech cards. This engine reliably finds primary attackers and heavily restricts the agent’s action space; with straightforward options, the heuristic stack avoids suboptimal branching paths.

**Resource Synergy**
Energy cards are kept to the strict mathematical minimum required to power primary attackers for six prizes. Instead of inflating the deck with excess Energy (which causes late-game dead draws), the strategy leverages explicit card synergies: specific Items are paired to recover Energy from the discard pile and accelerate it directly onto benched attackers. 

**Agent-Deck Alignment**
A rule-based agent struggles with control or disruption archetypes because they require deep probabilistic planning. By pairing the agent with a linear, aggressively costed deck, we offload the strategic burden from the code to the cards. The mathematically optimal play becomes the most obvious one, enabling the priority stack detailed in §4 to execute flawlessly.
