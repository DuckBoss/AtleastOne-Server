import pytest
from src.card import Card


class TestCard:
    def __init__(self):
        self.card = Card('regular', 'blue', 0, '#0000ff')
        pass

    def test_card_type(self):
        assert self.card.CardType == 'regular'

    def test_card_color(self):
        assert self.card.CardColor == 'blue'

    def test_card_number(self):
        assert self.card.CardNumber == 0

    def test_card_hex(self):
        assert self.card.CardHex == "#0000ff"
