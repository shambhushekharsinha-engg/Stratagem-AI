## 6. Meta Analysis & Empirical Findings (H5)

To evaluate archetype representation (H5), we parsed 4,741 episode logs from the August 16th dataset. Extracting reliable data required strict methodological rigor: naive state-array parsing initially flagged 15% of games as having "simultaneous" first prizes. Investigation revealed this to be an environment artifact—the engine compresses intermediate steps between agent decisions, batching turns together in the observation array. By parsing the raw, sequential game logs (tracking `fromArea == 6` prize-draws directly), we bypassed this artifact. This log-based extraction, combined with deduplicating multi-move cards, definitively accounted for 100% of the decisive dataset.

### The Aggro-Tempo Meta

Two high-tempo archetypes define the format:
1. **Dreepy / Drakloak**: 28.9% play rate, 53.6% win rate
2. **Teal Mask Ogerpon ex**: 18.0% play rate, 52.6% win rate

Combined, these two decks make up nearly half the field. Their positive win rates at such extreme play volumes confirm that early damage output is the dominant baseline strategy in the agent ecosystem.

### Rogue Variants

Despite the high-volume dominance of fast attackers, the highest empirical win rates in the top ten belong to slower variants. Due to our deterministic tie-joining fingerprint method, this archetype appears fragmented across distinct buckets: Slowpoke (67.0%, N=264), Slowpoke / Slowking (56.6%, N=509), and Slowpoke / Slowking / Mega Kangaskhan ex (58.0%, N=158). While the smaller sample sizes warrant caution, these elevated overall win rates suggest that resilient frameworks can successfully compete against the broader field, though explicit head-to-head matchup tracking would be required to prove a direct counter-strategy.
