import re
import csv
import os

_CARD_DICT = {}
try:
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'EN_Card_Data.csv')
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cid = int(row['Card ID'])
                if cid not in _CARD_DICT:
                    _CARD_DICT[cid] = []
                _CARD_DICT[cid].append(row)
            except:
                pass
except Exception:
    pass

import random

OPTIMAL_DECK = (
    [96]*4 + [916]*4 + [1]*12 + [1182]*4 + [1213]*4 + [1192]*4 + [1191]*4 + [1086]*4 + [1121]*4 + [1123]*4 + [1116]*4 + [1077]*4 + [1083]*4
)

class HeuristicAgent:
    def __init__(self):
        self.pending_action = None # Dict holding context: {'type': 'GUST', 'target': b_mon}
        self.gust_count = 0
        self.retreat_count = 0

    def __call__(self, obs, config):
        if obs.step == 0:
            return OPTIMAL_DECK
            
        select = obs.get('select', {})
        options = select.get('option', [])
        if not options: return []
        current = obs.get('current', {})

        # ---------------------------------------------------------
        # 0. Setup Phase Resolution (Types 1 and 9)
        # Type 9 = Select Active Pokemon
        # Type 1 = Select Bench Pokemon
        # ---------------------------------------------------------
        # 2. Setup Phase Logic
        # ---------------------------------------------------------
        if select.get('type') in [1, 9] and not self.pending_action:
            # Priority: Ogerpon ex (96) > Scyther (916)
            def setup_score(opt):
                # Type 1 uses 'index', Type 9 uses 'type' as the hand index in this engine
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

        # ---------------------------------------------------------
        # 1. Multi-Step Target Resolution
        if select.get('type') != 0:
            if self.pending_action:
                action_type = self.pending_action.get('type')
                
                if action_type == 'GUST':
                    target_idx = self.pending_action.get('target_idx')
                    for i, opt in enumerate(options):
                        if opt.get('index') == target_idx:
                            self.pending_action = None
                            return [i]
                    self.pending_action = None # Clear if not found to avoid lock
                            
                elif action_type == 'ENERGY_SWITCH':
                    # Prompt 1: Take FROM (Low value Pokemon)
                    # Prompt 2: Give TO (High value Pokemon)
                    step = self.pending_action.get('step', 1)
                    
                    # --- LIVE TRACE SAFETY NET ---
                    if not hasattr(self, 'eswitch_logs'): self.eswitch_logs = 0
                    if self.eswitch_logs < 3:
                        try:
                            with open('C:\\Stratagem-AI\\eswitch_live_trace.jsonl', 'a') as f:
                                import json
                                f.write(json.dumps({'step': step, 'obs_step': obs.get('step'), 'select': select}) + '\n')
                            if step == 2: self.eswitch_logs += 1
                        except: pass
                    # -----------------------------
                    
                    def eswitch_score(opt):
                        # Area 4 = Active, Area 5 = Bench
                        area = opt.get('area')
                        idx = opt.get('index')
                        if idx is None: return 0
                        p = current.get('players', [{}, {}])[current.get('yourIndex', 0)]
                        source_arr = []
                        if area == 4:
                            active = p.get('active')
                            source_arr = active if isinstance(active, list) else [active]
                        elif area == 5:
                            source_arr = p.get('bench', [])
                        
                        if idx < len(source_arr) and source_arr[idx]:
                            cid = source_arr[idx].get('id')
                            if cid == 96: return 100 # Ogerpon
                            if cid == 916: return 50 # Scyther
                        return 10
                        
                    scored_opts = sorted([(eswitch_score(opt), i) for i, opt in enumerate(options)], reverse=True)
                    
                    if step == 1:
                        self.pending_action['step'] = 2
                        # Take FROM lowest value (reverse sort order)
                        return [scored_opts[-1][1]] if scored_opts else [0]
                    else:
                        self.pending_action = None
                        # Give TO highest value
                        return [scored_opts[0][1]] if scored_opts else [0]
                            
                elif action_type == 'CARMINE_DISCARD':
                    min_count = select.get('minCount', 1)
                    
                    def get_card_id(opt):
                        if 'card_id' in opt: return opt['card_id']
                        area = opt.get('area')
                        idx = opt.get('index')
                        if idx is None: return None
                        source_arr = []
                        p = current.get('players', [{}, {}])[current.get('yourIndex', 0)]
                        if area == 1: source_arr = p.get('deck', [])
                        elif area == 2: source_arr = p.get('hand', [])
                        
                        if idx < len(source_arr):
                            card = source_arr[idx]
                            return card.get('id') if isinstance(card, dict) else card
                        return None
                        
                    def discard_score(opt):
                        cid = get_card_id(opt)
                        if cid in [1086, 1121, 1077, 1083]: return 10
                        if cid in [1182, 1213, 1192, 1191]: return 8  
                        if cid == 1: return 5                         
                        return 0                                      
                    
                    scored_opts = sorted([(discard_score(opt), i) for i, opt in enumerate(options)], reverse=True)
                    self.pending_action = None
                    return [idx for score, idx in scored_opts[:min_count]]

                elif action_type == 'SETUP_SEARCH':
                    min_count = select.get('minCount', 1)
                    step = self.pending_action.get('step', 1)
                    
                    def get_card_id(opt):
                        if 'card_id' in opt: return opt['card_id']
                        area = opt.get('area')
                        idx = opt.get('index')
                        if idx is None: return None
                        source_arr = []
                        p = current.get('players', [{}, {}])[current.get('yourIndex', 0)]
                        if area == 1: source_arr = p.get('deck', [])
                        elif area == 2: source_arr = p.get('hand', [])
                        
                        if idx < len(source_arr):
                            card = source_arr[idx]
                            return card.get('id') if isinstance(card, dict) else card
                        return None

                    if min_count > 1: # Discard prompt
                        def discard_score(opt):
                            cid = get_card_id(opt)
                            if cid in [1086, 1121, 1077, 1083]: return 10
                            if cid in [1182, 1213, 1192, 1191]: return 8  
                            if cid == 1: return 5                         
                            return 0                                      
                        
                        scored_opts = sorted([(discard_score(opt), i) for i, opt in enumerate(options)], reverse=True)
                        self.pending_action['step'] = 2 # Search prompt follows
                        return [idx for score, idx in scored_opts[:min_count]]
                    
                    else: # Search prompt
                        def search_score(opt):
                            cid = get_card_id(opt)
                            if cid == 96: return 100  
                            if cid == 916: return 50  
                            if cid == 1: return 20    
                            return 0
                        
                        scored_opts = sorted([(search_score(opt), i) for i, opt in enumerate(options)], reverse=True)
                        self.pending_action = None
                        return [scored_opts[0][1]] if scored_opts else [0]
                    
            # Fallback if no pending context
            min_req = select.get('minCount', 1)
            return list(range(min(min_req, len(options))))

        # Reset pending action when returning to main phase
        self.pending_action = None

        # ---------------------------------------------------------
        # 2. Main Phase Logic (Priorities 1-5)
        # ---------------------------------------------------------
        # (Assuming find_lethal_ko, get_affordable_attacks, etc. are defined as previously agreed)
        def is_play_boss(opt):
            # In actual execution, we resolve opt['index'] against the player's hand array to verify the card_id is 1182
            hand = current.get('players', [{}, {}])[current.get('yourIndex', 0)].get('hand', [])
            idx = opt.get('index')
            if idx is not None and idx < len(hand):
                card = hand[idx]
                card_id = card.get('id') if isinstance(card, dict) else card
                return card_id == 1182
            return False

        def is_play_setup_card(opt):
            hand = current.get('players', [{}, {}])[current.get('yourIndex', 0)].get('hand', [])
            idx = opt.get('index')
            if idx is not None and idx < len(hand):
                card = hand[idx]
                card_id = card.get('id') if isinstance(card, dict) else card
                # Poffin, Ultra Ball, Love Ball, Roto-Stick, Energy Switch, Carmine, Judge, Kieran
                return card_id in [1086, 1121, 1083, 1077, 1116, 1192, 1213, 1191]
            return False

        def is_attack_option(opt):
            return opt.get('type') == 13

        you_idx = current.get('yourIndex', 0)
        opp_idx = 1 - you_idx
        my_state = current.get('players', [{}, {}])[you_idx]
        opp_state = current.get('players', [{}, {}])[opp_idx]
        my_active = (my_state.get('active') or [None])[0]
        opp_active = (opp_state.get('active') or [None])[0]

        def get_affordable_attacks():
            return [opt for opt in options if is_attack_option(opt)]

        def calculate_projected_damage(atk_opt, attacker, target_mon):
            if not target_mon or not attacker: return 0
            base_dmg = get_opp_max_dmg(attacker)
            my_type = attacker.get('type')
            weakness = target_mon.get('weakness')
            resistance = target_mon.get('resistance')
            final_dmg = base_dmg
            if weakness and weakness == my_type: final_dmg *= 2
            if resistance and resistance == my_type: final_dmg -= 30
            return max(0, final_dmg)
            

        def get_opp_max_dmg(opp_act):
            if not opp_act: return 0
            cid = opp_act.get('id')
            energies = len(opp_act.get('energies', []))
            
            rows = _CARD_DICT.get(cid)
            if not rows: return 120
            
            max_d = 0
            for card in rows:
                dmg_str = str(card.get('Damage', '0'))
                m = re.search(r'\d+', dmg_str)
                base_dmg = int(m.group()) if m else 0
                
                cost_str = str(card.get('Cost', ''))
                cost_len = len(re.findall(r'\{[A-Z]\}|\u25cf', cost_str)) if cost_str and cost_str != 'nan' else 1
                
                effect = str(card.get('Effect Explanation', ''))
                
                if 'more damage for each' in effect or '+' in dmg_str or '×' in dmg_str:
                    potential = base_dmg + (30 * energies)
                    if potential > max_d: max_d = potential
                    continue
                    
                if energies >= cost_len and base_dmg > max_d:
                    max_d = base_dmg
                    
            return max_d

        def find_lethal_ko():
            my_prizes = len(my_state.get('prize', []))
            for i, opt in enumerate(options):
                if is_attack_option(opt) and opp_active:
                    dmg = calculate_projected_damage(opt, my_active, opp_active)
                    if opp_active.get('hp', 0) - opp_active.get('damage', 0) <= dmg:
                        prizes_taken = 2 if opp_active.get('is_ex') else 1
                        if prizes_taken >= my_prizes:
                            return i
            for i, opt in enumerate(options):
                if is_play_boss(opt):
                    affordable = get_affordable_attacks()
                    if not affordable or not my_active: continue
                    for b_idx, b_mon in enumerate(opp_state.get('bench', [])):
                        if not b_mon: continue
                        prizes_taken = 2 if b_mon.get('is_ex') else 1
                        if prizes_taken >= my_prizes:
                            for atk in affordable:
                                if b_mon.get('hp', 0) - b_mon.get('damage', 0) <= calculate_projected_damage(atk, my_active, b_mon):
                                    self.pending_action = {'type': 'GUST', 'target_idx': b_idx}
                                    return i
            return None

        def find_gust_ko():
            for i, opt in enumerate(options):
                if is_play_boss(opt):
                    affordable = get_affordable_attacks()
                    if not affordable or not my_active: continue
                    for b_idx, b_mon in enumerate(opp_state.get('bench', [])):
                        if not b_mon: continue
                        for atk in affordable:
                            if b_mon.get('hp', 0) - b_mon.get('damage', 0) <= calculate_projected_damage(atk, my_active, b_mon):
                                self.pending_action = {'type': 'GUST', 'target_idx': b_idx}
                                return i
            return None

        def find_active_ko():
            for i, opt in enumerate(options):
                if is_attack_option(opt) and opp_active:
                    dmg = calculate_projected_damage(opt, my_active, opp_active)
                    if opp_active.get('hp', 0) - opp_active.get('damage', 0) <= dmg:
                        return i
            return None

        def find_safe_retreat():
            if not my_active or not opp_active: return None
            remaining_hp = my_active.get('hp', 0) - my_active.get('damage', 0)
            opp_max_dmg = get_opp_max_dmg(opp_active)
            if remaining_hp <= opp_max_dmg:
                for i, opt in enumerate(options):
                    if opt.get('type') == 10:
                        for b_mon in my_state.get('bench', []):
                            if b_mon and (b_mon.get('hp', 0) - b_mon.get('damage', 0)) > opp_max_dmg:
                                return i
            return None
        def find_setup_or_damage():
            # Play setup items (e.g. Ultra Ball, Poffin, Supporters)
            for i, opt in enumerate(options):
                if is_play_setup_card(opt):
                    # Check specific cards for specialized state tracking
                    hand = current.get('players', [{}, {}])[current.get('yourIndex', 0)].get('hand', [])
                    idx = opt.get('index')
                    if idx is not None and idx < len(hand):
                        card = hand[idx]
                        cid = card.get('id') if isinstance(card, dict) else card
                        if cid == 1116:
                            self.pending_action = {'type': 'ENERGY_SWITCH', 'step': 1}
                            return i
                        if cid == 1192:
                            self.pending_action = {'type': 'CARMINE_DISCARD'}
                            return i
                    # Commit to resolving a search/setup action
                    self.pending_action = {'type': 'SETUP_SEARCH', 'step': 1}
                    return i
                    
            # Attach energy (Type 8)
            for i, opt in enumerate(options):
                if opt.get('type') == 8: return i
                
            # Attack for max damage
            max_atk_id = -1
            best_atk = None
            for i, opt in enumerate(options):
                if is_attack_option(opt):
                    atk_id = opt.get('attackId', 0)
                    if atk_id > max_atk_id:
                        max_atk_id = atk_id
                        best_atk = i
            if best_atk is not None:
                return best_atk
            return None

        lethal = find_lethal_ko()
        if lethal is not None: return [lethal]
        
        gust = find_gust_ko()
        if gust is not None:
            self.gust_count += 1
            return [gust]
        
        active_ko = find_active_ko()
        if active_ko is not None: return [active_ko]
        
        retreat = find_safe_retreat()
        if retreat is not None:
            self.retreat_count += 1
            return [retreat]
        
        setup_damage = find_setup_or_damage()
        if setup_damage is not None: return [setup_damage]

        return [random.randrange(len(options))]

# Required top-level function for kaggle_environments
_agent_instance = HeuristicAgent()
def agent(obs, config):
    return _agent_instance(obs, config)
