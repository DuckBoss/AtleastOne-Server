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
        # Retrieve all cards
        for card_color in data['cards']['colors']:
            for card_value in data['cards']['colors'][card_color]['values']:
                deck.append(Card(card_color=card_color, card_value=card_value, card_hex=data['cards']['colors'][card_color]['hex']))

    all_cards['all_cards'] = []
    for x in deck:
        all_cards['all_cards'].append(x)

    return all_cards['all_cards']
