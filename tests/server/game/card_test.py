from src.game.card import Card


class TestCard:
    def setup_method(self):
        self.card = Card(card_color='blue', card_value="0", card_hex='#0000ff')

    def teardown_method(self):
        del self.card

    def test_card_color(self):
        assert self.card.color == 'blue'

    def test_card_value(self):
        assert self.card.value == "0"

    def test_card_hex(self):
        assert self.card.hex == "#0000ff"
