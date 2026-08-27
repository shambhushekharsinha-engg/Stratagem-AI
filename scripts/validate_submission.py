"""
validate_submission.py — Pre-submission deck.csv validator.

DECK FORMAT (verified from SDK source: cabt.py + cg/game.py):
  - main.py reads deck.csv and expands it into a flat list[int] of 60 Card IDs.
  - The Kaggle runner does NOT perform this expansion — main.py must do it.
  - Column names 'card_id'/'count' are inferred (no official spec page exists).
    Verify against an official starter notebook if one is published.

CARD DATA SCHEMA (verified from EN_Card_Data.csv):
  - One row per MOVE, not one row per card.
  - Multi-attack Pokemon appear 2-3 times with the same Card ID.
  - 2,022 total rows | 1,267 unique Card IDs.
  - Validator deduplicates by Card ID before checking rules.

RULES VERIFIED FROM SDK SOURCE (cabt.py line 128, game.py line 31):
  - Exactly 60 total cards.
  - At least one Basic Pokemon.
  - Max 4 copies of any non-Basic-Energy card (Basic Energy is exempt).
"""

import pandas as pd
import os
import sys


def validate(deck_csv: str, cards_csv: str, verbose: bool = True) -> bool:
    if not os.path.exists(deck_csv):
        raise FileNotFoundError(f"Deck file not found: {deck_csv}")

    df = pd.read_csv(deck_csv)

    # Check 0: Column names
    if 'card_id' not in df.columns or 'count' not in df.columns:
        raise ValueError(
            f"deck.csv has unexpected columns {list(df.columns)}. "
            f"Expected 'card_id' and 'count'. "
            f"NOTE: column format is inferred, not officially specified."
        )

    # Check 1: Total = 60
    total = int(df['count'].sum())
    if total != 60:
        raise ValueError(f"Deck has {total} cards. Must be exactly 60.")

    # Load card db — deduplicate by Card ID (one row per card, not per move)
    cards = pd.read_csv(cards_csv)
    cards_unique = cards.groupby('Card ID').first().reset_index()
    stage_col = 'Stage (Pokémon)/Type (Energy and Trainer)'

    # Merge against deduplicated card db
    merged = df.merge(cards_unique, how='left', left_on='card_id', right_on='Card ID')

    # Check 2: All card_ids valid
    missing = merged[merged['Card ID'].isna()]['card_id'].tolist()
    if missing:
        raise ValueError(f"Unknown card_ids (not in EN_Card_Data.csv): {missing}")

    # Check 3: At least one Basic Pokemon
    if not any(merged[stage_col] == 'Basic Pokémon'):
        raise ValueError("Deck must contain at least one Basic Pokemon.")

    # Check 4: Max 4 copies of non-Basic-Energy cards
    violations = merged[
        (merged[stage_col] != 'Basic Energy') & (merged['count'] > 4)
    ][['card_id', 'Card Name', 'count']]
    if not violations.empty:
        msgs = [f"{row['Card Name']} (ID {row['card_id']}): {row['count']} copies"
                for _, row in violations.iterrows()]
        raise ValueError(f"Cards exceeding 4-copy limit: {'; '.join(msgs)}")

    # Check 5: Max 1 ACE SPEC card total
    ace_spec_count = merged[merged['Rule'] == 'ACE SPEC']['count'].sum()
    if ace_spec_count > 1:
        ace_specs = merged[merged['Rule'] == 'ACE SPEC'][['Card Name', 'count']]
        msgs = [f"{row['count']}x {row['Card Name']}" for _, row in ace_specs.iterrows()]
        raise ValueError(f"Deck has {ace_spec_count} ACE SPEC cards (limit 1): {', '.join(msgs)}")

    if verbose:
        print(f"[PASS] Validation PASSED: {deck_csv}")
        print(f"  Total cards: {total} | Unique entries: {len(df)}")
        print("  Deck contents:")
        for _, row in merged.iterrows():
            print(f"    {int(row['count']):2d}x  {row['Card Name']} (ID {row['card_id']}, {row[stage_col]})")

    return True


if __name__ == '__main__':
    deck = r'C:\Stratagem-AI\probe_submission\deck.csv'
    cards = r'C:\Stratagem-AI\data\EN_Card_Data.csv'
    try:
        validate(deck, cards)
    except (ValueError, FileNotFoundError) as e:
        print(f"[FAIL] Validation FAILED: {e}", file=sys.stderr)
        sys.exit(1)
