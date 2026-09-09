<div align="center">
  <img src="assets/stratagem_cover_photo.jpg" alt="Stratagem-AI Cover" width="100%">
  
  <br/>
  
  # Stratagem-AI: Advanced Heuristic Sequencing vs. Tempo in PTCG
  
  [![Interactive Paper](https://img.shields.io/badge/Interactive_Paper-Vercel-black?logo=vercel)](https://stratagem-ai-game.vercel.app/)
  [![YouTube Demo](https://img.shields.io/badge/Video_Walkthrough-YouTube-FF0000?logo=youtube)](https://www.youtube.com/watch?v=dU2HvTKX6Ww)
  [![Kaggle Submission](https://img.shields.io/badge/Kaggle-Writeup-20BEFF?logo=kaggle)](https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy/writeups/stratagem-tempo-dominance)
</div>

---

## ?? Video Walkthrough

[![Video Demo](assets/stratagem_ui_showcase_01.png)](https://www.youtube.com/watch?v=dU2HvTKX6Ww)
*(Click the image above to watch the full YouTube walkthrough)*

---

## 1. Abstract & Introduction

<img src="assets/stratagem_ui_showcase_02.png" align="right" width="45%" style="margin-left: 20px;">

This project investigates the necessity of complex sequential logic specifically defensive retreating and bench sniping in competitive Pokemon TCG (PTCG) environments. The dominant paradigm in card game AI often leans toward deep probabilistic search trees (like Monte Carlo Tree Search). However, we designed a highly optimized, five-tier heuristic agent capable of evaluating lethal thresholds and bench vulnerability in O(1) time complexity, hypothesizing it would significantly outperform a purely greedy baseline in a symmetrical, high-lethality mirror match. 

Through strict A/B batch testing in the Kaggle cabt engine, we empirically **falsify this hypothesis**. The heuristic agent achieved a 35.7% win rate (+/- 3.0% at 95% CI), finding itself structurally disadvantaged by its own defensive sequencing. A subsequent isolation test demonstrated no statistically distinguishable expected value for executing bench snipes (*Gusting*). Our findings prove that within a symmetric aggro archetype, raw tempo substantially outpaces complex decision-making; sacrificing attack turns or energy attachments for strategic positioning yields a net-negative expected value. Relentless Active damage maximization remains the empirically optimal strategy for the tested environment.

<div style="clear: both;"></div>

---

## 2. Game Theoretic & Mechanics Analysis

<img src="assets/stratagem_ui_showcase_04.png" align="right" width="45%" style="margin-left: 20px;">

Pokemon TCG is a stochastic, partial-information extensive-form game. Unlike chess or Go, the full game state is never visible. Each player sees only their own hand, their prize stack, and the shared public board.

### The Branching Factor Problem
This hidden information forces effective agents away from deterministic search toward probabilistic inference. The decision space is deceptively large. A single turn can chain draw Supporters (expanding the hand mid-turn), search Trainers, attach energy, and trigger abilities before finally resolving an attack. Attempting to use MCTS in this environment often leads to timeouts under the strict 30-minute Kaggle tournament constraints because the branching factor explodes exponentially with every drawn card. 

### The Prize Race Paradigm
Above all, PTCG is fundamentally a race. Six prizes are taken by dealing Knock Outs (KOs); there is no sustained healing mechanic in the current meta to reset momentum. This structural reality motivates our core hypothesis: **tempo dominates outcomes**. The agent that takes the first prize and sustains offensive pressure should theoretically win the overwhelming majority of games, regardless of minor positioning inefficiencies.

<div style="clear: both;"></div>

---

## 3. Deck Construction: Hardware as Strategy

<img src="assets/stratagem_ui_showcase_07.png" width="100%">

In constrained AI environments, the deck is the hardware and the Python agent is the software. Out of the 1,267 unique cards in the expanded pool, our deck was explicitly built to minimize the agent's decision-making complexity while maximizing tempo.

**Archetype and Consistency:**
We selected a fast, aggressive archetype focused exclusively on high-HP Basic attackers. Evolving Stage 1 and 2 Pokemon introduces mathematical variance and demands complex sequencing that heuristics struggle to execute perfectly. Heavy-hitting Basic Pokemon (*Ogerpon ex* and *Scyther*) ensure immediate pressure from turn one.

**Resource Synergy and Engine Alignment:**
Energy cards are kept to the strict mathematical minimum required to power primary attackers for six prizes. Instead of inflating the deck with excess Energy, the strategy leverages explicit card synergies. By pairing our rule-based agent with a linear, aggressively costed deck, we offloaded the strategic burden from the Python code directly into the card mechanics. Crucially, the supporter engine utilizing *Carmine* and *Judge* was selected to aggressively churn through the deck and disrupt the opponent's hand state, leaning entirely into raw offensive pacing.

---

## 4. Algorithmic Architecture (The 5-Tier Stack)

<img src="assets/stratagem_ui_showcase_08.png" align="right" width="45%" style="margin-left: 20px;">

The heuristic agent utilizes a five-tier priority stack evaluated sequentially each turn. Because it relies on boolean condition checks rather than forward-searching game trees, it executes decisions in < 1ms, completely immunizing it against Kaggle compute timeouts.

1. **Priority 1 (Lethal KO):** Explicitly checks for an immediate game-winning attack.
2. **Priority 2 (Gust Expected Value):** Evaluates the bench broadly, seeking positive prize trades or KOs on highly vulnerable targets.
3. **Priority 3 (Active KO):** Checks for lethal damage on the opponent's Active Pokemon.
4. **Priority 4 (Retreat & Preserve):** Evaluates if the agent's Active Pokemon is in lethal range. If true, swaps to a safe bench target.
5. **Priority 5 (Max Damage Fallback):** Executes setup actions or selects maximum damage.

### Bypassing Engine Limitations
<img src="assets/stratagem_ui_showcase_09.png" width="100%">

Damage evaluation requires a bifurcated approach due to engine limitations. The Kaggle cabt engine intentionally scrubs move-level metadata from its serialized observation states. To solve this, we implemented a custom damage projector. Rather than relying on the engine's scrubbed metadata, the agent dynamically parses the raw EN_Card_Data.csv to calculate true lethal thresholds.

<div style="clear: both;"></div>

---

## 5. Experimental Methodology & Rigor

<img src="assets/stratagem_ui_showcase_10.png" width="100%">

All experiments were conducted within the official Kaggle cabt engine. To ensure absolute statistical rigor and eliminate stochastic variance, our evaluations relied on strict control mechanisms:
* **Sample Size:** 1,000-game batch runs per isolated test.
* **Deterministic Seeding:** A fixed base seed of 42, incremented linearly per match.
* **Positional Parity (Seat Balancing):** 500 games played as Player 1, and 500 games played as Player 2. 
* **Confidence Intervals:** 95% Confidence Intervals calculated via the Wilson Score method.

---

## 6. Empirical Falsification (H1, H2, H3)

<img src="assets/stratagem_ui_showcase_11.png" align="right" width="45%" style="margin-left: 20px;">

**H1 & H2: Sequential Logic vs. Tempo Dominance**
Over 1,000 mirror matches, the heuristic stack achieved a **35.7% win rate** (+/- 3.0% at 95% CI), empirically falsifying H1. This strongly supports H2 (Tempo Dominance). The heuristic agent executed its defensive math flawlessly, triggering 993 sound retreats. However, retreating burns a turn and discards attached energy. The greedy baseline won **64.3%** of games by relentlessly optimizing for immediate Active damage.

**H3: Gust Expected Value (EV) Isolation**
A 1,000-game A/B test matching a No-Gust heuristic variant against the greedy baseline recorded a **36.0% win rate**. Bypassing the Active Pokemon to snipe the bench provided no measurable EV, largely because executing a Gust consumes the turn's single Supporter action (*Boss's Orders*), sacrificing critical setup power.

<div style="clear: both;"></div>

---

## 7. Environmental Dependency (Cross-Archetype Robustness)

<img src="assets/stratagem_ui_showcase_12.png" width="100%">

To evaluate if the heuristic's failure was an artifact of the symmetric tempo mirror, we pitted our heuristic aggro agent against the greedy baseline operating two distinct alternative archetypes: an Evolution/Spread deck (*Dragapult ex*) and a Control/Stall deck (*Slowking*).

**Findings:** The data establishes a substantial environmental dependency. We hypothesize that in the highly lethal *Ogerpon ex* mirror, the opportunity cost of retreating is mathematically prohibitive. Against slower, development-reliant setups like *Dragapult* and *Slowking*, the tempo penalty of defensive sequencing is naturally absorbed, resulting in statistical ties (51.3% and 49.0% win rates).

---

## 8. Meta Analysis & Log Parsing Pipeline

<img src="assets/stratagem_ui_showcase_14.png" width="100%">

To evaluate broader archetype representation across the competition, we engineered a custom data pipeline to parse **4,741 episode logs** from the August 16th Kaggle dataset.

**The Aggro-Tempo Meta**
Two high-tempo archetypes define the format: *Dreepy / Drakloak* (28.9% play rate) and *Teal Mask Ogerpon ex* (18.0% play rate). Combined, these two decks make up nearly half the field, validating our hypothesis that early damage output is the dominant baseline strategy.

**Rogue Variants**
Despite the dominance of fast attackers, the highest empirical win rates in the top ten belong to slower variants like *Slowpoke* (67.0%, N=264). These elevated win rates suggest that highly resilient control frameworks can successfully compete against the broader field if piloted correctly.

---

## 9. Conclusions

<img src="assets/stratagem_ui_showcase_15.png" width="100%">

Our rigorous testing within the Kaggle cabt engine demonstrates that in high-lethality mirror matches, **tempo dictates victory over sequential positioning**. Retreating wounded attackers and sniping bench targets wastes critical resources and surrenders momentum to a purely greedy baseline. 

Furthermore, our codebase represents an extraordinarily lightweight, Kaggle-compliant solution. Operating in O(1) time complexity without the need for expensive Monte Carlo rollouts, our heuristic engine provides an empirically proven baseline for future researchers looking to optimize Tempo-based strategies in Trading Card Game AI.
