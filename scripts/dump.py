import json
with open('skim_logs.json') as f: data = json.load(f)
steps = data['p0_loss']
for i in range(len(steps)-5, len(steps)):
    obs = steps[i][0]['observation']
    p0 = steps[i][0]
    p1 = steps[i][1]
    c0 = obs['current']['players'][0]
    c1 = obs['current']['players'][1]
    
    a0 = c0.get('active', [{}])[0] if c0.get('active') else {}
    a1 = c1.get('active', [{}])[0] if c1.get('active') else {}
    
    deck0 = len(c0.get('deck', []))
    deck1 = len(c1.get('deck', []))
    prize0 = len(c0.get('prize', []))
    prize1 = len(c1.get('prize', []))
    
    print(f'\n--- STEP {i} ---')
    print(f'P0: {p0["status"]} Act: {p0.get("action")} | Deck: {deck0}, Prizes: {prize0}')
    print(f'P1: {p1["status"]} Act: {p1.get("action")} | Deck: {deck1}, Prizes: {prize1}')
    if i == len(steps)-1:
        print('Rewards P0:', p0['reward'], 'P1:', p1['reward'])
