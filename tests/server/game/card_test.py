from src.game.card import Card


class TestCard:
    def setup_method(self):
        self.card = Card(card_category='regular', card_color='blue', card_number=0, card_hex='#0000ff')

    def teardown_method(self):
        del self.card

    def test_card_type(self):
        assert self.card.category == 'regular'

    def test_card_color(self):
        assert self.card.color == 'blue'

    def test_card_number(self):
        assert self.card.number == 0

    def test_card_hex(self):
        assert self.card.hex == "#0000ff"
