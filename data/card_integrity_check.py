import pandas as pd, sys
sys.stdout.reconfigure(encoding='utf-8')
cards = pd.read_csv(r'C:\Stratagem-AI\data\EN_Card_Data.csv')
stage_col = 'Stage (Pokémon)/Type (Energy and Trainer)'

# Check 1: exact nunique
print(f'Exact nunique Card ID: {cards["Card ID"].nunique()}')
print()

# Check 2: unique per category (post-dedup)
unique = cards.groupby('Card ID').first().reset_index()
print('Per-category unique card counts:')
cat_counts = unique[stage_col].value_counts().sort_values(ascending=False)
print(cat_counts.to_string())
print(f'Sum: {cat_counts.sum()}')
print()

# Check 3: Item duplicates specifically
print('Item Card ID duplication (rows per ID):')
item_mask = cards[stage_col] == 'Item'
item_dup = cards[item_mask].groupby('Card ID').size().value_counts()
print(item_dup.to_string())
print()

# Show the duplicate Item rows
item_dups = cards[item_mask].groupby('Card ID').filter(lambda x: len(x) > 1)
print('Duplicate Item rows (all):')
print(item_dups[['Card ID','Card Name','Expansion','Move Name','Effect Explanation']].to_string())
