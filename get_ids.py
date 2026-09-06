import csv

key_cards = ["Dreepy", "Drakloak", "Dragapult ex", "Slowpoke", "Slowking", "Psychic Energy", "Kieran", "Professor's Research", "Nest Ball", "Ultra Ball", "Iono", "Buddy-Buddy Poffin"]

with open('data/EN_Card_Data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Card Name', '').strip()
        if any(kc in name for kc in key_cards):
            print(f"ID: {row['Card ID']} | Name: {name} | Category: {row.get('Category', '')}")
