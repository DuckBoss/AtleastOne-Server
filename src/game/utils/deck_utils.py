import json
from src.game.card import Card
import os


all_cards = {}
path_to_current_file = os.path.realpath(__file__)
current_directory = os.path.split(path_to_current_file)[0]
json_path = os.path.join(current_directory, '../../definitions/cards.json')


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
        all_cards['all_cards'].append(x)

    return all_cards['all_cards']
