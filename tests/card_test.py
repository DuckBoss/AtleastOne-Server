from src.card import Card


class TestCard:
    def setup_method(self):
        self.card = Card('regular', 'blue', 0, '#0000ff')

    def teardown_method(self):
        del self.card

    def test_card_type(self):
        assert self.card.CardType == 'regular'

    def test_card_color(self):
        assert self.card.CardColor == 'blue'

    def test_card_number(self):
        assert self.card.CardNumber == 0

    def test_card_hex(self):
        assert self.card.CardHex == "#0000ff"
