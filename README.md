# Stratagem-AI 

[![Vercel Deploy](https://img.shields.io/badge/Vercel-Hosted_Paper-black?style=for-the-badge&logo=vercel)](https://stratagem-ai-game.vercel.app/)
[![Kaggle](https://img.shields.io/badge/Kaggle-Strategy_Submission-blue?style=for-the-badge&logo=kaggle)](https://www.kaggle.com/competitions/pokemon-tcg-ai-battle-challenge-strategy)

**Stratagem-AI** is a submission for the Kaggle Pokémon TCG AI Battle Challenge (Strategy Category). 

This repository contains the full empirical research, A/B testing infrastructure, and heuristic agents developed to falsify the hypothesis that deep sequential reasoning (defensive retreating and bench sniping) outperforms greedy tempo optimization in high-lethality mirror matches.

## 📄 The Research Paper

The formal 7-section Kaggle Writeup submission is hosted here: 
👉 **[View the Hosted Research Paper](https://stratagem-ai-game.vercel.app/)**

The paper outlines:
- **Hypothesis Testing**: Falsification of sequential priority stacks vs. baseline tempo.
- **Agent Design**: A 5-tier heuristic priority stack bypassing cabt engine limitations.
- **A/B Batch Simulations**: Results of 1,000-game isolated environment tests.
- **Meta Analysis**: Parsing 4,700+ episode logs for empirical archetype representation.

## 📂 Repository Structure
- \PAPER.md\: The raw markdown of the 7-section Kaggle Strategy writeup.
- \public/\: Frontend assets for the Vercel-hosted portfolio site.
- \heuristic_agent.py\: The primary 5-tier heuristic agent (H1).
- \heuristic_agent_no_gust.py\: The ablation-tested variant isolating expected value of Priority 2 (H3).
- \greedy_agent.py\: The relentless damage-maximizing baseline (H2).
- \data/\, \docs/\, \logs/\, \scripts/\: Supporting infrastructure and empirical game logs.

## 🚀 Execution & Reproducibility
The agents in this repository are built to run inside Kaggle's \cabt\ C++ environment. All metrics reported in the paper were drawn from deterministic 1,000-game batch runs against the greedy baseline in identical setup environments.
