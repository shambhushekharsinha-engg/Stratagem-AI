"""
deck_builder_minimal.py — Generates a legal deck.csv from EN_Card_Data.csv.

IMPORTANT — CARD DATA SCHEMA:
  EN_Card_Data.csv has ONE ROW PER MOVE, not one row per card.
  Multi-attack cards (most Pokemon) appear 2-3 times with the same Card ID.
  Total rows: 2,022 | Unique Card IDs: 1,267

  All analysis must groupby('Card ID').first() to get one row per card,
  or groupby('Card ID') to aggregate (e.g., max HP, all move names).

DECK FORMAT — VERIFIED FROM SDK SOURCE (cabt.py + cg/game.py):
  - The engine (battle_start) receives a flat list[int] of exactly 60 Card IDs with repeats.
  - deck.csv (card_id, count) is a COMPACT representation that main.py must expand itself.
  - The Kaggle runner does NOT expand deck.csv — main.py is responsible for reading it
    and returning the flat 60-length list on step 0 (when obs["select"] is None).
  - Column names 'card_id' / 'count' are inferred from SDK default deck convention
    and beginner guide; no official spec page confirms them — still partially unverified.
"""

import pandas as pd
import os


def build_minimal_deck(csv_path: str, out_path: str) -> list[int]:
    """
    Build and write a minimal legal deck.csv.
    Returns the expanded flat list[int] for verification.
    """
    cards = pd.read_csv(csv_path)
    stage_col = 'Stage (Pokémon)/Type (Energy and Trainer)'

    # One row per card: groupby Card ID, take first row (avoids multi-move duplicates)
    unique_cards = cards.groupby('Card ID').first().reset_index()

    # Pick highest-HP Basic Pokemon
    basics = unique_cards[unique_cards[stage_col] == 'Basic Pokémon'].copy()
    basics['HP_num'] = pd.to_numeric(basics['HP'], errors='coerce')
    top_basic = basics.sort_values('HP_num', ascending=False).iloc[0]
    top_basic_id = int(top_basic['Card ID'])

    # Pick first Basic Energy
    energies = unique_cards[unique_cards[stage_col] == 'Basic Energy']
    energy_id = int(energies.iloc[0]['Card ID'])

    # Write compact deck.csv (2 rows)
    deck_rows = [
        {'card_id': top_basic_id, 'count': 4},
        {'card_id': energy_id,    'count': 56},
    ]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pd.DataFrame(deck_rows).to_csv(out_path, index=False)
    print(f"deck.csv written: 4x {top_basic['Card Name']} (ID {top_basic_id}), 56x Energy (ID {energy_id})")

    # Return expanded flat list — what main.py must return on step 0
    flat = [top_basic_id] * 4 + [energy_id] * 56
    assert len(flat) == 60
    return flat


if __name__ == '__main__':
    flat = build_minimal_deck(
        r'C:\Stratagem-AI\data\EN_Card_Data.csv',
        r'C:\Stratagem-AI\probe_submission\deck.csv'
    )
    print(f"Flat deck (first 10 IDs): {flat[:10]} ... (total: {len(flat)})")
