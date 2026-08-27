"""
main.py — Minimal Simulation Category agent.

DECK PROTOCOL (from SDK source cabt.py + cg/game.py):
  On step 0, obs["select"] is None. The agent must return a flat list[int]
  of exactly 60 Card IDs (with repeats). The runner does NOT read deck.csv —
  main.py reads it and expands it here.

  deck.csv format: two columns 'card_id' (int) and 'count' (int),
  rows summing to 60. The compact format is expanded into a repeated flat list.
"""

import random
import csv
import os

AGENT_DIR = '/kaggle_simulations/agent/'


def load_deck(deck_path: str) -> list[int]:
    """Read deck.csv and expand into flat list[int] of 60 Card IDs."""
    deck = []
    with open(deck_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            deck.extend([int(row['card_id'])] * int(row['count']))
    if len(deck) != 60:
        raise ValueError(f"deck.csv expanded to {len(deck)} cards, expected 60.")
    return deck


# Load deck at import time (once per episode, not per turn)
_deck_path = os.path.join(AGENT_DIR, 'deck.csv')
_DECK = load_deck(_deck_path)


def agent(observation, configuration):
    """
    Minimal random agent.
    Step 0: return deck (list[int] of 60 card IDs).
    All other steps: return random legal option.
    """
    if observation.get('select') is None:
        return _DECK
    options = observation['select']['option']
    max_count = observation['select']['maxCount']
    return random.sample(range(len(options)), max_count)
