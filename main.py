import random 

default_deck = {
    'shuffle_time': False,
    'idx': 0,
    'cards': [
        { 'mod': 'crit', 'benefit': 'crit', 'crit': True },
        { 'mod': 'miss', 'miss': True },
        { 'mod': 2 },
        { 'mod': -2 },
        { 'mod': 1 },
        { 'mod': 1 },
        { 'mod': 1 },
        { 'mod': 1 },
        { 'mod': 1 },
        { 'mod': -1 },
        { 'mod': -1 },
        { 'mod': -1 },
        { 'mod': -1 },
        { 'mod': -1 },
        { 'mod': 0 },
        { 'mod': 0 },
        { 'mod': 0 },
        { 'mod': 0 },
        { 'mod': 0 },
        { 'mod': 0 }
    ]
}

deck = default_deck.copy()

def remove_card(deck, card):
    idx = deck['cards'].index(card)
    deck['cards'].pop(idx)

def add_card(deck, card):
    deck["cards"].append(card)

def shuffle(deck):
    deck['idx'] = 0
    deck['shuffle_time'] = False
    random.shuffle(deck['cards'])

def isempty(deck):
    return deck['idx'] > len(deck['cards'])
    
def draw(deck):
    if isempty(deck):
        return False
    idx = deck['idx']
    card = deck['cards'][idx]
    deck['idx'] += 1
    if card['mod'] == 'crit' or card['mod'] == 'miss':
        deck['shuffle_time'] = True
    return card

def isrolling(card):
    if 'rolling' in card.keys():
        return card['rolling']
    return False
    
def hasbenefit(card):
    if 'benefit' in card.keys():
        return True
    return False
    
def issamebenefit(card1,card2):
    return card1['benefit'] == card2['benefit']
    
def iscrit(card):
    return 'crit' in card.keys() 

def ismiss(card):
    return 'miss' in card.keys()

def weakestcard(card1, card2):
    if card1['mod'] <= card2['mod']:
        return card1
    return card2
    
def strongestcard(card1, card2):
    if card1['mod'] <= card2['mod']:
        return card2
    return card1

def retcard(card):
    c = {
        'mod': card['mod'],
        'benefit': 1 if hasbenefit(card) else 0
    }
    if ismiss(card):
        c['miss'] = True
    if iscrit(card):
        c['crit'] = True
    return c

def attackdraw(deck, advantage = False, disadvantage = False):
    rolling = []
    card = draw(deck)
    while isrolling(card):
        rolling += [card]
        card = draw(deck)
    
    extra = False
    if advantage or disadvantage:
        extra = draw(deck)
            
    if disadvantage:
        # Disadvantage
        if not extra:
            return retcard(card)
        cards = [card,extra]
        if any(map(ismiss,cards)):
            return {
                'mod': 'miss',
                'benefit': 0,
                'miss': True
            }
        if all(map(hasbenefit,cards)):
            if issamebenefit(*cards) and not iscrit(card):
                return retcard(weakestcard(*cards))
            return retcard(card)
        if any(map(hasbenefit,cards)):
            if any(map(iscrit,cards)):
                if iscrit(card):
                    return retcard(extra)
                return retcard(card)
            if hasbenefit(weakestcard(*cards)):
                return retcard(card)
        return retcard(weakestcard(*cards))
        
    totrolling = 0
    totbenefits = 0
    for card in rolling:
        totrolling += card['mod']
        if hasbenefit(card):
            totbenefits += 1
    
    if not advantage or not extra:
        # Regular
        if ismiss(card):
            return retcard(card)
        if iscrit(card):
            return {
                'mod': totrolling,
                'benefit': totbenefits,
                'crit': True
            }
        card = retcard(card)
        card['mod'] += totrolling
        card['benefit'] += totbenefits
        return card
        
    # Advantage
    cards = [card,extra]
    if any(map(iscrit, cards)):
        return {
            'mod': totrolling,
            'benefit': totbenefits,
            'crit': True
        }
    if any(map(ismiss, cards)):
        if ismiss(card):
            card = retcard(extra)
            card['mod'] += totrolling
            card['benefit'] += totbenefits
            return card
        card = retcard(card)
        card['mod'] += totrolling
        card['benefit'] += totbenefits
        return card
    card = strongestcard(*cards)
    card = retcard(card)
    card['mod'] += totrolling
    card['benefit'] += totbenefits
    return card
    
def calcatk(base, card):
    if ismiss(card):
        return (0, 0)
    atk = base + card['mod']
    if iscrit(card):
        atk *= 2
    return (atk, card['benefit'])

if __name__ == '__main__':
    N = int(1e5)
    shuffle(deck)
    
    advantage = False
    disadvantage = False
    base_atk = 2
    sample_atk = []
    sample_ben = []
    
    # Berserker perks
    if 0:
        remove_card(deck, {'mod': -1})
        remove_card(deck, {'mod': -1})
    
    if 0:
        remove_card(deck, {'mod': 0})
        remove_card(deck, {'mod': 0})
        remove_card(deck, {'mod': 0})
        remove_card(deck, {'mod': 0})
        
    for _ in range(0): # up to 2
        remove_card(deck, {'mod': -1})
        add_card(deck, {'mod': 1})
    
    for _ in range(2): # up to 2
        remove_card(deck, {'mod': 0})
        add_card(deck, {'mod': +2, 'rolling': True})
        
    for _ in range(1): # up to 2
        for _ in range(2):
            add_card(deck, {'mod': 0, 'benefit': 'wound', 'rolling': True})

    for _ in range(0): # up to 2
        add_card(deck, {'mod': 0, 'benefit': 'stun', 'rolling': True})
    
    if 0:
        add_card(deck, {'mod': 1, 'benefit': 'disarm', 'rolling': True})
    
    if 0:
        add_card(deck, {'mod': 0, 'benefit': 'heal', 'rolling': True})
    
    for _ in range(0): # up to 2
        add_card(deck, {'mod': 2, 'benefit': 'fire', 'rolling': True})
    
    # Loop
    for n in range(N):
        card = attackdraw(deck, advantage, disadvantage)
        atk, ben = calcatk(base_atk, card)
        sample_atk += [atk]
        sample_ben += [ben]
        
        if deck['shuffle_time']:
            shuffle(deck)
    
    atk_avg = sum(sample_atk)/N
    ben_avg = sum(sample_ben)/N
    atk_var = sum(map(lambda x: (x - atk_avg)**2, sample_atk))/N
    
    print(f'Avg. atk.: {atk_avg}')
    print(f'Avg. std.: {atk_var ** (.5)}')
    print(f'Avg. ben.: {ben_avg}')
        
    