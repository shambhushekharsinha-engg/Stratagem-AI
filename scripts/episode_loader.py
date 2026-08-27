import json
import os
import pandas as pd

def load_deduped_cards():
    df = pd.read_csv(r'C:\Stratagem-AI\data\EN_Card_Data.csv')
    unique_cards = df.groupby('Card ID').first().reset_index()
    return unique_cards.set_index('Card ID').to_dict('index')

def identify_archetype(deck_list, card_dict):
    pokemon_counts = {}
    valid_stages = {'Basic Pokémon', 'Stage 1 Pokémon', 'Stage 2 Pokémon'}
    
    for cid in deck_list:
        card = card_dict.get(cid)
        if card:
            stage_val = str(card.get('Stage (Pokémon)/Type (Energy and Trainer)', ''))
            if stage_val in valid_stages:
                pokemon_counts[cid] = pokemon_counts.get(cid, 0) + 1
            
    if not pokemon_counts:
        return "No Pokémon"
        
    max_count = max(pokemon_counts.values())
    signature_ids = [cid for cid, count in pokemon_counts.items() if count == max_count]
    signature_ids.sort() 
    
    names = [card_dict[cid]['Card Name'] for cid in signature_ids]
    return " / ".join(names)

def parse_episodes():
    card_dict = load_deduped_cards()
    directory = r'C:\Stratagem-AI\data\episodes'
    files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Counters for dropped/skipped episodes
    cnt_total = len(files)
    cnt_json_err = 0
    cnt_short = 0
    cnt_unresolved_reward = 0
    cnt_invalid_deck = 0
    cnt_no_first_prize_found = 0
    valid_decks_counted = 0
    
    first_prize_wins = 0
    first_prize_losses = 0
    first_prize_draws = 0
    
    archetype_stats = {}
    
    print(f"Parsing {cnt_total} episodes...")
    
    for f_name in files:
        path = os.path.join(directory, f_name)
        with open(path, encoding='utf-8') as f:
            try:
                data = json.load(f)
            except:
                cnt_json_err += 1
                continue
                
        steps = data.get('steps', [])
        if len(steps) < 2:
            cnt_short += 1
            continue
            
        last_step = steps[-1]
        r0 = last_step[0].get('reward')
        r1 = last_step[1].get('reward')
        
        winner = None
        if r0 == 1: winner = 0
        elif r1 == 1: winner = 1
        elif r0 == 0 and r1 == 0: winner = -1
        
        if winner is None:
            cnt_unresolved_reward += 1
            continue
            
        deck0 = steps[1][0].get('action', [])
        deck1 = steps[1][1].get('action', [])
        
        if isinstance(deck0, list) and len(deck0) == 60 and isinstance(deck1, list) and len(deck1) == 60:
            valid_decks_counted += 2
            arch0 = identify_archetype(deck0, card_dict)
            arch1 = identify_archetype(deck1, card_dict)
            
            for arch in [arch0, arch1]:
                if arch not in archetype_stats:
                    archetype_stats[arch] = {'wins': 0, 'losses': 0, 'draws': 0}
            
            if winner == 0:
                archetype_stats[arch0]['wins'] += 1
                archetype_stats[arch1]['losses'] += 1
            elif winner == 1:
                archetype_stats[arch1]['wins'] += 1
                archetype_stats[arch0]['losses'] += 1
            elif winner == -1:
                archetype_stats[arch0]['draws'] += 1
                archetype_stats[arch1]['draws'] += 1
        else:
            cnt_invalid_deck += 1

        # H2 Track First Prize via Logs
        # Kaggle environment compresses steps between decisions, so state arrays can show simultaneous prize drops.
        # The logs maintain strict sequential ordering. fromArea == 6 represents drawing from the Prize zone.
        first_taker = None
        for step in steps:
            for log in step[0].get('observation', {}).get('logs', []):
                if log.get('fromArea') == 6:
                    first_taker = log.get('playerIndex')
                    break
            if first_taker is not None:
                break
                
        if first_taker is not None and winner is not None:
            if winner == -1:
                first_prize_draws += 1
            elif first_taker == winner:
                first_prize_wins += 1
            else:
                first_prize_losses += 1
        else:
            cnt_no_first_prize_found += 1

    print(f"\n=== Parse Summary ===")
    print(f"Total files: {cnt_total}")
    print(f"  JSON errors: {cnt_json_err}")
    print(f"  Short episodes (<2 steps): {cnt_short}")
    print(f"  Unresolved rewards: {cnt_unresolved_reward}")
    print(f"  Invalid deck lengths: {cnt_invalid_deck}")
    print(f"  No prize taken: {cnt_no_first_prize_found}")
    print(f"  Valid decks counted: {valid_decks_counted}")
    
    assert cnt_json_err + cnt_short + cnt_unresolved_reward + cnt_no_first_prize_found + (first_prize_wins + first_prize_losses + first_prize_draws) == cnt_total, "Accounting mismatch!"

    print("\n=== H2: Tempo Advantage (First Prize) ===")
    total_decisive = first_prize_wins + first_prize_losses
    if total_decisive > 0:
        win_rate = (first_prize_wins / total_decisive) * 100
        print(f"Games where first-prize taker won: {first_prize_wins}")
        print(f"Games where first-prize taker lost: {first_prize_losses}")
        print(f"Games where first-prize taker drew: {first_prize_draws}")
        print(f"First-prize win rate: {win_rate:.1f}%")
        
    print("\n=== H5: Archetype Meta (Top 10) ===")
    sorted_archs = sorted(archetype_stats.items(), 
                          key=lambda x: x[1]['wins'] + x[1]['losses'] + x[1]['draws'], 
                          reverse=True)
                          
    for arch, stats in sorted_archs[:10]:
        total = stats['wins'] + stats['losses'] + stats['draws']
        wr = (stats['wins'] / (stats['wins'] + stats['losses'])) * 100 if (stats['wins'] + stats['losses']) > 0 else 0
        print(f"{arch[:40]:<40} | Play Rate: {(total/valid_decks_counted)*100:.1f}% | Win Rate: {wr:.1f}% ({total} games)")

if __name__ == '__main__':
    parse_episodes()
