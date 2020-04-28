import json
from card import Card

json_path = 'definitions/cards.json'
json_path_spec = 'definitions/card-specials.json'

deck = []
all_cards = {}
with open(json_path, 'r') as card_defs:
    data = json.load(card_defs)
    # Retrieve colored cards
    for card_color in data['cards']['colors']:
        print(f"{card_color} - "
              f"\n{data['cards']['colors'][card_color]['numbers']}"
              f"\n{data['cards']['colors'][card_color]['special']}")
        for card_number in data['cards']['colors'][card_color]['numbers']:
            deck.append(Card('regular', card_color, card_number=card_number, card_hex=data['cards']['colors'][card_color]['hex']))
        for card_number in data['cards']['colors'][card_color]['special']:
            deck.append(Card('regular', card_color, card_number=card_number, card_hex=data['cards']['colors'][card_color]['hex']))
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
with open('test_files/all-cards.json', 'w') as out_file:
    json.dump(all_cards, out_file)

print('\n'.join(x.get_json_dump() for x in deck))
print(f'Deck Size: {len(deck)}')
