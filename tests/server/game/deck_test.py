from src.game.card import Card
from src.game.deck import Deck


class TestDeck:
    def setup_method(self):
        self.card_1 = Card(card_category='regular', card_color='blue', card_number=0, card_hex='#0000ff')
        self.card_2 = Card(card_category='skip', card_color='white', card_hex='#ffffff')
        self.card_3 = Card(card_category='regular', card_color='green', card_number=5, card_hex='#aaabbb')
        self.card_4 = Card(card_category='regular', card_color='blue', card_number=1, card_hex='#222ddd')
        self.card_5 = Card(card_category='reverse', card_color='red', card_hex='#555dda')
        self.card_6 = Card(card_category='regular', card_color='yellow', card_number=8, card_hex='#7dd643')

        self.deck = Deck(max_deck_size=10, cards=[self.card_1, self.card_2, self.card_3, self.card_4, self.card_5, self.card_6])

    def teardown_method(self):
        del self.card_1, self.card_2, self.card_3, self.card_4, self.card_5, self.card_6
        del self.deck

    def test_deck_size(self):
        assert self.deck.size == 6

    def test_deck_regular_cards(self):
        count = 0
        for x in range(self.deck.size):
            item = self.deck.draw()
            if item.category == 'regular':
                count += 1
        assert count == 4

    def test_deck_red_cards(self):
        count = 0
        for x in range(self.deck.size):
            card = self.deck.draw()
            if card.color == 'red':
                count += 1
        assert count == 1

    def test_deck_random_card(self):
        card = self.deck.draw_random()
        assert card.hex != ''
