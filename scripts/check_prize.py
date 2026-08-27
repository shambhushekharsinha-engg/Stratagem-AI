import json
with open(r'C:\Stratagem-AI\data\episodes\93459410.json', encoding='utf-8') as f:
    data = json.load(f)
for i in [82, 83, 84, 85]:
    c = data['steps'][i][0]['observation'].get('current')
    if c:
        p0 = c['players'][0].get('prize', [])
        p1 = c['players'][1].get('prize', [])
        print(f"Step {i}")
        print(f"  P0 prize length: {len(p0)}, contents: {p0}")
        print(f"  P1 prize length: {len(p1)}, contents: {p1}")
