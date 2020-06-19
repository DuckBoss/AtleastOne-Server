import json
from src.game.card import Card
from src.game.deck import Deck

json_path = 'definitions/cards.json'
json_path_spec = 'definitions/card-specials.json'

deck = Deck()
all_cards = {}
with open(json_path, 'r') as card_defs:
    data = json.load(card_defs)
    # Retrieve all cards
    for card_color in data['cards']['colors']:
        print(f"{card_color} - "
              f"\n{data['cards']['colors'][card_color]['values']}")
        for card_number in data['cards']['colors'][card_color]['values']:
            deck.add_to_top(Card(card_color=card_color, card_value=card_number, card_hex=data['cards']['colors'][card_color]['hex']))

all_cards['all_cards'] = []
for x in list(deck.deck):
    item = x.get_json()
    all_cards['all_cards'].append(item)
with open('test_files/test-all-cards.json', 'w') as out_file:
    json.dump(all_cards, out_file)

print('\n'.join(x.get_json_dump() for x in list(deck.deck)))
print(f'Deck Size: {len(deck.deck)}')
