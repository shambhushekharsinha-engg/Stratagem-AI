# H5 Cross-Archetype Robustness - Canonical Execution Log

**Date:** 2026-09-06
**Engine:** Kaggle cabt environment
**Configuration:** 1,000 games per matchup (N=1000)
**Positional Balancing:** 500 games with Heuristic Agent as Player 1, 500 games as Player 2
**Stochastic Control:** Deterministic seed schedule (Base Seed 42, incremented per game)

## Raw Counts

### H1: Aggro Mirror
*   **Test:** Heuristic Aggro vs Greedy Aggro
*   **Base Seed:** 42
*   **Heuristic Wins (P1):** 161/500
*   **Heuristic Wins (P2):** 196/500
*   **Total Heuristic Wins:** 357 (35.7%)
*   **Total Baseline Wins:** 643 (64.3%)
*   **Ties:** 0
*   **95% CI:** ±3.0%

### H5a: Evolution / Spread
*   **Test:** Heuristic Aggro vs Greedy Baseline operating Dragapult ex
*   **Deck Configuration (Midrange):** 4x Dreepy (119), 4x Drakloak (120), 4x Dragapult ex (121), 6x Fire Energy (2), 6x Psychic Energy (5), 36x Baseline Trainers.
*   **Base Seed:** 10042
*   **Heuristic Wins (P1):** 235/500
*   **Heuristic Wins (P2):** 278/500
*   **Total Heuristic Wins:** 513 (51.3%)
*   **Total Baseline Wins:** 487 (48.7%)
*   **Ties:** 0
*   **95% CI:** ±3.1%

### H5b: Control / Stall
*   **Test:** Heuristic Aggro vs Greedy Baseline operating Slowking
*   **Deck Configuration (Control):** 4x Slowpoke (162), 4x Slowking (163), 16x Psychic Energy (5), 36x Baseline Trainers.
*   **Base Seed:** 20042
*   **Heuristic Wins (P1):** 223/500
*   **Heuristic Wins (P2):** 267/500
*   **Total Heuristic Wins:** 490 (49.0%)
*   **Total Baseline Wins:** 510 (51.0%)
*   **Ties:** 0
*   **95% CI:** ±3.1%

## Methodological Note: The 40.9% Transition
Early exploratory batches in the cabt engine yielded an unseeded, positionally-unbalanced 40.9% heuristic win rate in the H1 mirror. Following a rigorous methodology audit, the canonical pipeline was upgraded to enforce strict P1/P2 seat balancing and deterministic seed schedules to eliminate stochastic drift. The 35.7% result recorded above represents the final, strictly controlled evaluation.
