import json
import os
from src.game.card import Card
from src.game.deck import Deck


class TestJSON:
    def setup_method(self):
        path_to_current_file = os.path.realpath(__file__)
        current_directory = os.path.split(path_to_current_file)[0]
        self.json_path = os.path.join(current_directory, '../src/test_files/test-default-cards.json')
        self.deck = Deck(108)
        self.all_cards = {}

    def teardown_method(self):
        del self.json_path
        del self.deck
        del self.all_cards

    def test_json(self):
        with open(self.json_path, 'r') as card_defs:
            data = json.load(card_defs)
            # Retrieve all cards
            for card_color in data['cards']['colors']:
                print(f"{card_color} - "
                      f"\n{data['cards']['colors'][card_color]['numbers']}"
                      f"\n{data['cards']['colors'][card_color]['special']}")
                for card_value in data['cards']['colors'][card_color]['numbers']:
                    self.deck.add_to_top(Card(card_color=card_color, card_value=card_value,
                                     card_hex=data['cards']['colors'][card_color]['hex']))
        self.all_cards['all_cards'] = []
        for x in list(self.deck.deck):
            item = x.get_json()
            self.all_cards['all_cards'].append(item)
        assert len(self.all_cards['all_cards']) == 108

