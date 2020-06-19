from typing import List, Optional
from src.game.card import Card


class Player:
    def __init__(self, socket, name, hand=Optional[List[Card]]):
        self._socket = socket
        self._name = name
        self._hand = hand

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, value: Optional[List[Card]]):
        self._hand = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def socket(self):
        return self._socket
