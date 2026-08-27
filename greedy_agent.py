import random

OPTIMAL_DECK = (
    [96]*4 + [916]*4 +      # Teal Mask Ogerpon ex (96), Scyther (916)
    [1]*12 +                # 12x Grass Energy
    [1182]*4 + [1213]*4 +   # Boss's Orders, Judge
    [1192]*4 + [1191]*4 +   # Carmine, Kieran
    [1086]*4 + [1121]*4 +   # Buddy-Buddy Poffin, Ultra Ball
    [1123]*4 + [1116]*4 +   # Switch, Energy Switch
    [1077]*4 + [1083]*4     # Roto-Stick, Love Ball
)

def greedy_agent(obs, config):
    if obs.step == 0:
        return OPTIMAL_DECK
    
    select = obs.get('select', {})
    options = select.get('option', [])
    if not options:
        return []

    current = obs.get('current', {})

    if select.get('type') in [1, 9]:
        def setup_score(opt):
            idx = opt.get('index') if 'index' in opt else opt.get('type')
            hand = current.get('players', [{}, {}])[current.get('yourIndex', 0)].get('hand', [])
            if idx is not None and idx < len(hand):
                card = hand[idx]
                cid = card.get('id') if isinstance(card, dict) else card
                if cid == 96: return 100
                if cid == 916: return 50
            return 0
            
        scored_opts = sorted([(setup_score(opt), i) for i, opt in enumerate(options)], reverse=True)
        min_req = select.get('minCount', 1)
        if scored_opts:
            return [idx for score, idx in scored_opts[:min_req]]
        return list(range(min(min_req, len(options))))

    def is_attack_option(opt):
        return opt.get('type') == 13

    # 1. Attach energy if available
    for i, opt in enumerate(options):
        if opt.get('type') == 8:
            return [i]

    # 2. Maximize damage (Pick highest attackId, which correlates to higher damage/energy requirements in CABT)
    max_atk_id = -1
    best_opt = None
    for i, opt in enumerate(options):
        if is_attack_option(opt):
            atk_id = opt.get('attackId', 0)
            if atk_id > max_atk_id:
                max_atk_id = atk_id
                best_opt = i
                
    if best_opt is not None:
        return [best_opt]
        
    return [random.randrange(len(options))]
