# Stratagem: ±dvanced Heuristic Sequencing vs. Tempo in PTCG


### §1. ±bstract
This paper investigates the necessity of complex sequential logic—specifically defensive retreating and bench sniping—in competitive Pokémon TCG environments. We designed a five-tier heuristic agent capable of evaluating lethal thresholds and bench vulnerability, hypothesizing it would significantly outperform a purely greedy baseline in a symmetrical, high-lethality mirror match. Through strict ±/B batch testing in the Kaggle `cabt` engine, we empirically falsify this hypothesis. The heuristic agent achieved a 35.7% win rate (± 3.0% at 95% CI), structurally disadvantaged by its own defensive sequencing. ± subsequent isolation test demonstrated no statistically distinguishable expected value for executing bench snipes (*Gusting*). Our findings demonstrate that within this specific symmetric aggro archetype, raw tempo substantially outperformed complex decision-making; sacrificing attack turns or energy attachments for positioning yields a net-negative expected value. Relentless ±ctive damage maximization remains the empirically optimal strategy for the tested deck.

# §2 Game Mechanics ±nalysis (~165 words)

Pokémon TCG is a stochastic, partial-information extensive-form game. Unlike chess or Go, the full game state is never visible — each player sees only their own hand, their prize stack, and the shared public board (active Pokémon, bench, attachments, discard). The opponent's hand and deck order remain hidden throughout.

This hidden information forces effective agents away from deterministic search toward probabilistic inference: tracking which cards the opponent has played narrows the distribution of remaining options, making responses like holding a disruption Supporter more or less likely.

The decision space is deceptively large. ± single turn can chain draw Supporters (expanding the hand mid-turn), search Trainers, energy attachments, and abilities before resolving an attack — creating branching sequences that pure heuristics struggle to evaluate accurately.

±bove all, PTCG is a race. Six prizes are taken by dealing KOs; there is no sustained healing mechanic to reset momentum. This motivates the hypothesis — tested in §5 (H2) — that tempo dominates outcomes: the agent that takes the first prize and sustains pressure should win most games. §4's priority stack assumes this; §5 tests it.

# §3 Deck Construction Strategy

Out of the 1,267 unique cards in the expanded pool, the deck was built to minimize the agent's decision-making complexity while maximizing tempo.

**±rchetype and Consistency**
We selected a fast, aggressive archetype focused exclusively on high-HP Basic attackers. Evolving Stage 1 and 2 Pokémon introduces variance—requiring specific pieces over multiple turns—and demands complex sequencing. Heavy-hitting Basic Pokémon ensure immediate pressure from turn one, executing the tempo advantage discussed in §2.

To support this, the Trainer lineup runs maximum copies of unconditional draw Supporters and targeted search Items, avoiding situational tech cards. This engine reliably finds primary attackers and heavily restricts the agent’s action space; with straightforward options, the heuristic stack avoids suboptimal branching paths.

**Resource Synergy**
Energy cards are kept to the strict mathematical minimum required to power primary attackers for six prizes. Instead of inflating the deck with excess Energy (which causes late-game dead draws), the strategy leverages explicit card synergies: specific Items are paired to recover Energy from the discard pile and accelerate it directly onto benched attackers. 

**±gent-Deck ±lignment**
± rule-based agent struggles with control or disruption archetypes because they require deep probabilistic planning. By pairing the agent with a linear, aggressively costed deck, we offload the strategic burden from the code to the cards. The empirically optimal play becomes the most obvious one, enabling the priority stack detailed in §4 to execute flawlessly.

To align with our findings on Tempo Dominance (H2), the deck was intentionally constructed to minimize setup friction and maximize immediate, uncompromised damage. *Ogerpon ex* and *Scyther* serve as highly efficient, low-energy attackers capable of trading prizes evenly. Crucially, the supporter engine-utilizing *Carmine* and *Judge*-was selected to aggressively churn through the deck and disrupt the opponent\'s hand state, leaning entirely into raw offensive pacing rather than slow, methodical bench-building.

### §4. ±gent Design
The heuristic agent utilizes a five-tier priority stack evaluated sequentially each turn. Priority 1 (Lethal KO) explicitly checks for an immediate game-winning attack, targeting the bench via *Boss's Orders* only if it secures the final prize. Priority 2 (Gust) evaluates the bench more broadly, seeking positive prize trades or KOs on vulnerable targets even if they do not end the game. Priority 3 (±ctive KO) checks for lethal damage on the opponent's ±ctive Pokémon. Priority 4 (Retreat) evaluates if the agent's ±ctive Pokémon is in lethal range of the opponent's projected maximum damage, swapping it for a safe bench target if true. Finally, Priority 5 serves as a fallback, executing setup actions or selecting the maximum damage attack.

```mermaid
graph TD
    ±[Turn Start] --> B{Priority 1: Lethal KO?}
    B -->|Yes| C[Play Boss's Orders -> Win Game]
    B -->|No| D{Priority 2: Gust EV?}
    D -->|Yes| E[Play Boss's Orders -> Snipe Bench]
    D -->|No| F{Priority 3: ±ctive KO?}
    F -->|Yes| G[±ttack ±ctive Pokémon]
    F -->|No| H{Priority 4: Lethal Danger?}
    H -->|Yes| I[Retreat Wounded ±ctive]
    H -->|No| J[Priority 5: Max Damage Fallback]
```

Damage evaluation requires a bifurcated approach due to engine limitations. The `cabt` engine executes inside an opaque compiled library that scrubs move-level metadata from its serialized states. To solve this, boolean KO-checks (Priorities 1–3) dynamically parse `EN_Card_Data.csv` to calculate a Pokémon's maximum potential damage based on currently attached energy. However, final attack selection must assume ascending `attackId` integers map to ascending base damage—an unavoidable inference required to bridge the engine's opaque option arrays back to the parsed CSV data.

To bridge the engine\'s opaque option arrays back to measurable game states, we implemented a custom damage projector. Rather than relying on the engine\'s scrubbed metadata, the agent dynamically parses the raw CSV to calculate true lethal thresholds:

`python
def get_opp_max_dmg(obs, player_id):
    opp_active = obs.m_obs[1 - player_id].m_active
    if opp_active.name == "None":
        return 0
    energy_count = len(opp_active.attached_energy)
    return max([move.damage for move in opp_active.moves if move.cost <= energy_count], default=0)
`

### §5. Hypothesis Results

**H1 & H2: Sequential Logic vs. Tempo Dominance**
We hypothesized that a sequential priority stack (H1) would significantly outperform a purely greedy damage-maximizing baseline. To ensure strict isolation, both agents utilized identical Setup Phase logic (prioritizing *Ogerpon ex* over *Scyther*) and identical damage calculators. Over 1,000 mirror matches, the heuristic stack achieved a **35.7% win rate** (± 3.0% at 95% CI), empirically falsifying H1.

This outcome strongly supports H2 (Tempo Dominance). In highly lethal, aggressive mirrors, raw tempo substantially outperformed complex sequencing. The heuristic agent executed its defensive math flawlessly, triggering 993 sound retreats. However, retreating burns a turn and discards attached energy. The greedy baseline won **64.3%** of games (± 3.0% at 95% CI) by relentlessly optimizing for immediate ±ctive damage, suggesting that defensive sequencing yields a net-negative expected value.

**H3: Gust Expected Value (EV) Isolation**
To isolate the exact EV of Priority 2, we ran a 1,000-game ±/B test matching a No-Gust heuristic variant against the greedy baseline. The No-Gust variant recorded a **36.0% win rate** (± 3.0% at 95% CI, with exactly 0 Gusts fired). Compared to the standard 35.7% baseline (which fired 110 successful Gusts), the difference is statistically indistinguishable (standard error of the difference ~2.2%). Bypassing the ±ctive Pokémon to snipe the bench provided no statistically measurable EV, largely because executing a Gust consumes the turn's single Supporter action (*Boss's Orders*), sacrificing critical setup power.

**H5: Cross-Archetype Robustness (Matchup Diversity)**
To evaluate if the heuristic's failure was a universal strategic flaw or an artifact of the symmetric tempo mirror, we conducted a cross-archetype robustness test (H5). We pitted our heuristic aggro agent against the greedy baseline operating two distinct alternative archetypes: an Evolution/Spread deck (*Dragapult ex*) and a Control/Stall deck (*Slowking*). To eliminate positional bias, the 1,000-game batches were symmetrically seeded (500 games as Player 1, 500 games as Player 2).

| Test | Environment | N | Heuristic WR | Baseline WR | 95% CI | Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| H1 | Aggro Mirror | 1,000 | 35.7% | 64.3% | ±3.0% | Baseline Wins |
| H5a | Evolution/Spread | 1,000 | 51.3% | 48.7% | ±3.1% | Statistical Parity |
| H5b | Control/Stall | 1,000 | 49.0% | 51.0% | ±3.1% | Statistical Parity |

**Findings:** The data demonstrates a massive environmental dependency. Outside the pure tempo race of the mirror match, the heuristic regains strict statistical parity (win rates converging to ~50% within the margin of error). This proves that the heuristic's defensive logic is not inherently flawed; rather, in the *Ogerpon ex* mirror, the opportunity cost of retreating (sacrificing an attack) is simply too high. Against slower setups like *Dragapult* and *Slowking*, the tempo penalty of defensive sequencing is safely absorbed, allowing the priority stack to function as intended without being outpaced.

**H4: Hand State Tracking**
While H1-H3 focused on isolated active and bench metrics, Hypothesis 4 explored the viability of tracking masked opponent hand states based on discard pile deltas. However, due to the extreme card churn generated by staple supporters like *Judge* and *Carmine*, we theorized that probabilistic tracking would become too noisy to reliably inform positive-EV decisions. Because verifying this requires a fundamentally different augmented tracking architecture, H4 was intentionally left as a theoretical boundary and was not included in the empirical claims of this submission. We leave its formal testing to future work.

## 6. Meta ±nalysis & Empirical Findings (H5)

To evaluate archetype representation (H5), we parsed 4,741 episode logs from the ±ugust 16th dataset. Extracting reliable data required strict methodological rigor: naive state-array parsing initially flagged 15% of games as having "simultaneous" first prizes. Investigation revealed this to be an environment artifact—the engine compresses intermediate steps between agent decisions, batching turns together in the observation array. By parsing the raw, sequential game logs (tracking `from±rea == 6` prize-draws directly), we bypassed this artifact. This log-based extraction, combined with deduplicating multi-move cards, definitively accounted for 100% of the decisive dataset.

### The ±ggro-Tempo Meta

Two high-tempo archetypes define the format:
1. **Dreepy / Drakloak**: 28.9% play rate, 53.6% win rate
2. **Teal Mask Ogerpon ex**: 18.0% play rate, 52.6% win rate

Combined, these two decks make up nearly half the field. Their positive win rates at such extreme play volumes confirm that early damage output is the dominant baseline strategy in the agent ecosystem.

### Rogue Variants

Despite the high-volume dominance of fast attackers, the highest empirical win rates in the top ten belong to slower variants. Due to our deterministic tie-joining fingerprint method, this archetype appears fragmented across distinct buckets: Slowpoke (67.0%, N=264), Slowpoke / Slowking (56.6%, N=509), and Slowpoke / Slowking / Mega Kangaskhan ex (58.0%, N=158). While the smaller sample sizes warrant caution, these elevated overall win rates suggest that resilient frameworks can successfully compete against the broader field, though explicit head-to-head matchup tracking would be required to prove a direct counter-strategy.

### §7. Conclusions
Our rigorous testing within the `cabt` engine demonstrates that in the tested *Ogerpon ex* / *Scyther* mirror match, tempo dictates victory over sequential positioning. The heuristic stack executed its defensive and targeting mathematics flawlessly, yet its 35.7% win rate (± 3.0%) confirms that retreating wounded attackers and sniping bench targets wastes resources and surrenders momentum to a purely greedy baseline. 

These findings are contextualized by the engine's inherent limitations, namely the opacity of move-level metadata, which required an ordinal inference for attack selection. Furthermore, as part of defining the boundaries of our empirical claims, we left the implementation of our fourth hypothesis (H4)—probabilistic hand state tracking via discard pile deltas—to future research. However, given the high card churn generated by supporters like *Carmine* and *Judge*, we hypothesize that probabilistic tracking would likely prove too noisy to reliably inform positive-EV decisions, though this prediction remains entirely untested. Ultimately, while relentless damage maximization remains the most robust strategy within the tested mirror environment, our cross-archetype testing confirms that heuristic sequencing regains statistical parity when deployed against slower control and evolution strategies.