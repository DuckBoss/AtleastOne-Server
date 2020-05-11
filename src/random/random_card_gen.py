import json
import random
import copy
import time
from src.game.card import Card
from src.game.deck import Deck

all_cards = {}
json_path = '../definitions/cards.json'

def generate_card_dictionary():
    deck = []
    with open(json_path, 'r') as card_defs:
        data = json.load(card_defs)
        # Retrieve colored cards
        for card_color in data['cards']['colors']:
            print(f"{card_color} - "
                  f"\n{data['cards']['colors'][card_color]['numbers']}"
                  f"\n{data['cards']['colors'][card_color]['special']}")
            for card_number in data['cards']['colors'][card_color]['numbers']:
                deck.append(Card(card_category='regular', card_color=card_color, card_number=card_number, card_hex=data['cards']['colors'][card_color]['hex']))
            for card_type in data['cards']['colors'][card_color]['special']:
                deck.append(Card(card_category=card_type, card_color=card_color, card_number=-1, card_hex=data['cards']['colors'][card_color]['hex']))
        # Retrieve uncolored cards
        for unique in data['cards']['unique']:
            for i in range(int(data['cards']['unique'][unique]['amount'])):
                print(f"{unique} - "
                      f"\n{data['cards']['unique'][unique]}")
                deck.append(Card(unique, 'none', card_number=-1, card_hex=data['cards']['unique'][unique]['hex']))

    all_cards['all_cards'] = []
    for x in deck:
        item = x.get_json()
        all_cards['all_cards'].append(item)


# Generate the card dictionary (list of every card available)
generate_card_dictionary()

random_picked_cards = {}
for i in range(0, 2000000):
    random.seed(random.random())
    picked_card_index = random.randint(0, len(all_cards['all_cards'])-1)
    picked_card = copy.deepcopy(list(all_cards['all_cards'])[picked_card_index])
    print(picked_card)
    try:
        random_picked_cards[picked_card['id']] += 1
    except KeyError:
        random_picked_cards[picked_card['id']] = 1

print(random_picked_cards)


sum = 0
for i in random_picked_cards.values():
    sum += i
print(sum)

