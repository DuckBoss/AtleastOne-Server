import json
from src.game.card import Card
from src.game.deck import Deck

json_path = 'definitions/cards.json'
json_path_spec = 'definitions/card-specials.json'

deck = Deck()
all_cards = {}
with open(json_path, 'r') as card_defs:
    data = json.load(card_defs)
    # Retrieve colored cards
    for card_color in data['cards']['colors']:
        print(f"{card_color} - "
              f"\n{data['cards']['colors'][card_color]['numbers']}"
              f"\n{data['cards']['colors'][card_color]['special']}")
        for card_number in data['cards']['colors'][card_color]['numbers']:
            deck.add_to_top(Card(card_category='regular', card_color=card_color, card_number=card_number, card_hex=data['cards']['colors'][card_color]['hex']))
        for card_type in data['cards']['colors'][card_color]['special']:
            deck.add_to_top(Card(card_category=card_type, card_color=card_color, card_number=-1, card_hex=data['cards']['colors'][card_color]['hex']))
    # Retrieve uncolored cards
    for unique in data['cards']['unique']:
        for i in range(int(data['cards']['unique'][unique]['amount'])):
            print(f"{unique} - "
                  f"\n{data['cards']['unique'][unique]}")
            deck.add_to_top(Card(unique, 'none', card_number=-1, card_hex=data['cards']['unique'][unique]['hex']))

all_cards['all_cards'] = []
for x in list(deck.deck):
    item = x.get_json()
    all_cards['all_cards'].append(item)
with open('test_files/test-all-cards.json', 'w') as out_file:
    json.dump(all_cards, out_file)

print('\n'.join(x.get_json_dump() for x in list(deck.deck)))
print(f'Deck Size: {len(deck.deck)}')
