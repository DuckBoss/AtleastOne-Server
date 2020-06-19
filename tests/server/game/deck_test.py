from src.game.card import Card
from src.game.deck import Deck


class TestDeck:
    def setup_method(self):
        self.card_1 = Card(card_color='blue', card_value=0, card_hex='#0000ff')
        self.card_2 = Card( card_color='green', card_value=5, card_hex='#aaabbb')
        self.card_3 = Card(card_color='blue', card_value=1, card_hex='#222ddd')
        self.card_4 = Card(card_color='red', card_hex='#555dda')
        self.card_5 = Card(card_color='yellow', card_value=8, card_hex='#7dd643')
        self.card_6 = Card(card_color='black', card_value='wild', card_hex='#000000')

        self.deck = Deck(max_deck_size=10, cards=[self.card_1, self.card_2, self.card_3, self.card_4, self.card_5, self.card_6])

    def teardown_method(self):
        del self.card_1, self.card_2, self.card_3, self.card_4, self.card_5, self.card_6
        del self.deck

    def test_deck_size(self):
        assert self.deck.size == 6

    def test_deck_cards(self):
        count = 0
        for x in range(self.deck.size):
            self.deck.draw()
            count += 1
        assert count == 6

    def test_deck_random_card(self):
        card = self.deck.draw_random()
        assert card.hex != ''
