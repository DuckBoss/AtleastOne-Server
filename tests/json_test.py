import json
import os
from src.game.card import Card


class TestJSON:
    def setup_method(self):
        path_to_current_file = os.path.realpath(__file__)
        current_directory = os.path.split(path_to_current_file)[0]
        self.json_path = os.path.join(current_directory, '../src/test_files/test-default-cards.json')
        self.deck = []
        self.all_cards = {}

    def teardown_method(self):
        del self.json_path
        del self.deck
        del self.all_cards

    def test_json(self):
        with open(self.json_path, 'r') as card_defs:
            data = json.load(card_defs)
            # Retrieve colored cards
            for card_color in data['cards']['colors']:
                print(f"{card_color} - "
                      f"\n{data['cards']['colors'][card_color]['numbers']}"
                      f"\n{data['cards']['colors'][card_color]['special']}")
                for card_number in data['cards']['colors'][card_color]['numbers']:
                    self.deck.append(Card(card_category='regular', card_color=card_color, card_number=card_number,
                                     card_hex=data['cards']['colors'][card_color]['hex']))
                for card_special in data['cards']['colors'][card_color]['special']:
                    self.deck.append(Card(card_category=card_special, card_color=card_color, card_number=-1,
                                     card_hex=data['cards']['colors'][card_color]['hex']))
            # Retrieve uncolored cards
            for unique in data['cards']['unique']:
                for i in range(int(data['cards']['unique'][unique]['amount'])):
                    print(f"{unique} - "
                          f"\n{data['cards']['unique'][unique]}")
                    self.deck.append(Card(card_category=unique, card_color='none', card_number=-1, card_hex=data['cards']['unique'][unique]['hex']))

        self.all_cards['all_cards'] = []
        for x in self.deck:
            item = x.get_json()
            self.all_cards['all_cards'].append(item)
        assert len(self.all_cards['all_cards']) == 108

