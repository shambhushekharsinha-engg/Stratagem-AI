# Stratagem: Advanced Heuristic Sequencing vs. Tempo in PTCG


### §1. Abstract
This paper investigates the necessity of complex sequential logic—specifically defensive retreating and bench sniping—in competitive Pokémon TCG environments. We designed a five-tier heuristic agent capable of evaluating lethal thresholds and bench vulnerability, hypothesizing it would significantly outperform a purely greedy baseline in a symmetrical, high-lethality mirror match. Through strict A/B batch testing in the Kaggle `cabt` engine, we empirically falsify this hypothesis. The heuristic agent achieved a 40.9% win rate, structurally disadvantaged by its own defensive sequencing. A subsequent isolation test proved that executing bench snipes (*Gusting*) provided zero measurable expected value. Our findings demonstrate that within this specific symmetric aggro archetype, raw tempo strictly dominates complex decision-making; sacrificing attack turns or energy attachments for positioning yields a net-negative expected value. Relentless Active damage maximization remains the mathematically superior strategy for the tested deck.

# §2 Game Mechanics Analysis (~165 words)

Pokémon TCG is a stochastic, partial-information extensive-form game. Unlike chess or Go, the full game state is never visible — each player sees only their own hand, their prize stack, and the shared public board (active Pokémon, bench, attachments, discard). The opponent's hand and deck order remain hidden throughout.

This hidden information forces effective agents away from deterministic search toward probabilistic inference: tracking which cards the opponent has played narrows the distribution of remaining options, making responses like holding a disruption Supporter more or less likely.

The decision space is deceptively large. A single turn can chain draw Supporters (expanding the hand mid-turn), search Trainers, energy attachments, and abilities before resolving an attack — creating branching sequences that pure heuristics struggle to evaluate accurately.

Above all, PTCG is a race. Six prizes are taken by dealing KOs; there is no sustained healing mechanic to reset momentum. This motivates the hypothesis — tested in §5 (H2) — that tempo dominates outcomes: the agent that takes the first prize and sustains pressure should win most games. §4's priority stack assumes this; §5 tests it.

# §3 Deck Construction Strategy

Out of the 1,267 unique cards in the expanded pool, the deck was built to minimize the agent's decision-making complexity while maximizing tempo.

**Archetype and Consistency**
We selected a fast, aggressive archetype focused exclusively on high-HP Basic attackers. Evolving Stage 1 and 2 Pokémon introduces variance—requiring specific pieces over multiple turns—and demands complex sequencing. Heavy-hitting Basic Pokémon ensure immediate pressure from turn one, executing the tempo advantage discussed in §2.

To support this, the Trainer lineup runs maximum copies of unconditional draw Supporters and targeted search Items, avoiding situational tech cards. This engine reliably finds primary attackers and heavily restricts the agent’s action space; with straightforward options, the heuristic stack avoids suboptimal branching paths.

**Resource Synergy**
Energy cards are kept to the strict mathematical minimum required to power primary attackers for six prizes. Instead of inflating the deck with excess Energy (which causes late-game dead draws), the strategy leverages explicit card synergies: specific Items are paired to recover Energy from the discard pile and accelerate it directly onto benched attackers. 

**Agent-Deck Alignment**
A rule-based agent struggles with control or disruption archetypes because they require deep probabilistic planning. By pairing the agent with a linear, aggressively costed deck, we offload the strategic burden from the code to the cards. The mathematically optimal play becomes the most obvious one, enabling the priority stack detailed in §4 to execute flawlessly.

### §4. Agent Design
The heuristic agent utilizes a five-tier priority stack evaluated sequentially each turn. Priority 1 (Lethal KO) explicitly checks for an immediate game-winning attack, targeting the bench via *Boss's Orders* only if it secures the final prize. Priority 2 (Gust) evaluates the bench more broadly, seeking positive prize trades or KOs on vulnerable targets even if they do not end the game. Priority 3 (Active KO) checks for lethal damage on the opponent's Active Pokémon. Priority 4 (Retreat) evaluates if the agent's Active Pokémon is in lethal range of the opponent's projected maximum damage, swapping it for a safe bench target if true. Finally, Priority 5 serves as a fallback, executing setup actions or selecting the maximum damage attack.

Damage evaluation requires a bifurcated approach due to engine limitations. The `cabt` engine executes inside an opaque compiled library that scrubs move-level metadata from its serialized states. To solve this, boolean KO-checks (Priorities 1–3) dynamically parse `EN_Card_Data.csv` to calculate a Pokémon's maximum potential damage based on currently attached energy. However, final attack selection must assume ascending `attackId` integers map to ascending base damage—an unavoidable inference required to bridge the engine's opaque option arrays back to the parsed CSV data.

### §5. Hypothesis Results

**H1 & H2: Sequential Logic vs. Tempo Dominance**
We hypothesized that a sequential priority stack (H1) would significantly outperform a purely greedy damage-maximizing baseline. To ensure strict isolation, both agents utilized identical Setup Phase logic (prioritizing *Ogerpon ex* over *Scyther*) and identical damage calculators. Over 1,000 mirror matches, the heuristic stack achieved a **40.9% win rate**, empirically falsifying H1.

This outcome strongly supports H2 (Tempo Dominance). In highly lethal, aggressive mirrors, raw tempo strictly dominates complex sequencing. The heuristic agent executed its defensive math flawlessly, triggering 993 sound retreats. However, retreating burns a turn and discards attached energy. The greedy baseline won 59.1% of games by relentlessly optimizing for immediate Active damage, proving that defensive sequencing yields a net-negative expected value.

**H3: Gust Expected Value (EV) Isolation**
To isolate the exact EV of Priority 2, we ran a 1,000-game A/B test matching a No-Gust heuristic variant against the greedy baseline. The No-Gust variant recorded a **41.2% win rate** (and exactly 0 Gusts fired). Compared to the standard 40.9% baseline (which fired 110 successful Gusts), the difference is statistical noise. Bypassing the Active Pokémon to snipe the bench provided zero measurable EV, largely because executing a Gust consumes the turn's single Supporter action (*Boss's Orders*), sacrificing critical setup power.

**H4: Hand State Tracking**
[TBD: Awaiting implementation of an augmented tracking agent and corresponding 1,000-game batch run to measure isolated EV. Hypothesis testing will focus on whether tracking masked opponent hand states based on discard pile deltas remains viable, or if the high card churn from *Judge* and *Carmine* renders probabilistic tracking too noisy to inform positive-EV decisions.]

## 6. Meta Analysis & Empirical Findings (H5)

To evaluate archetype representation (H5), we parsed 4,741 episode logs from the August 16th dataset. Extracting reliable data required strict methodological rigor: naive state-array parsing initially flagged 15% of games as having "simultaneous" first prizes. Investigation revealed this to be an environment artifact—the engine compresses intermediate steps between agent decisions, batching turns together in the observation array. By parsing the raw, sequential game logs (tracking `fromArea == 6` prize-draws directly), we bypassed this artifact. This log-based extraction, combined with deduplicating multi-move cards, definitively accounted for 100% of the decisive dataset.

### The Aggro-Tempo Meta

Two high-tempo archetypes define the format:
1. **Dreepy / Drakloak**: 28.9% play rate, 53.6% win rate
2. **Teal Mask Ogerpon ex**: 18.0% play rate, 52.6% win rate

Combined, these two decks make up nearly half the field. Their positive win rates at such extreme play volumes confirm that early damage output is the dominant baseline strategy in the agent ecosystem.

### Rogue Variants

Despite the high-volume dominance of fast attackers, the highest empirical win rates in the top ten belong to slower variants. Due to our deterministic tie-joining fingerprint method, this archetype appears fragmented across distinct buckets: Slowpoke (67.0%, N=264), Slowpoke / Slowking (56.6%, N=509), and Slowpoke / Slowking / Mega Kangaskhan ex (58.0%, N=158). While the smaller sample sizes warrant caution, these elevated overall win rates suggest that resilient frameworks can successfully compete against the broader field, though explicit head-to-head matchup tracking would be required to prove a direct counter-strategy.

### §7. Conclusions
Our rigorous testing within the `cabt` engine demonstrates that in the tested *Ogerpon ex* / *Scyther* mirror match, tempo dictates victory over sequential positioning. The heuristic stack executed its defensive and targeting mathematics flawlessly, yet its 40.9% win rate confirms that retreating wounded attackers and sniping bench targets wastes resources and surrenders momentum to a purely greedy baseline. 

These findings are contextualized by the engine's inherent limitations, namely the opacity of move-level metadata, which required an ordinal inference for attack selection. Furthermore, due to time and scope constraints, we did not implement and test our fourth hypothesis (H4), which proposed that probabilistically tracking masked hand states via discard pile deltas would yield positive expected value. We leave the construction of this augmented hand-tracking agent to future research. However, given the high card churn generated by supporters like *Carmine* and *Judge*, we hypothesize that probabilistic tracking would likely prove too noisy to reliably inform positive-EV decisions, though this prediction remains entirely untested. Ultimately, relentless damage maximization remains the optimal proven strategy for this specific archetype.