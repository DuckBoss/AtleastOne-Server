from typing import List, Optional
from src.game.card import Card
from src.game.deck import Deck
from src.server.server_client import Client


class Player(Client):
    def __init__(self, socket, name, hand: Optional[List[Card]] = None):
        super().__init__(socket, name)
        self._hand = hand if hand is not None else Deck()

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, deck: Optional[List[Card]]):
        self._hand = deck

    def add_to_hand(self, card: Card):
        self._hand.add_to_top(card)

    def remove_from_hand(self, card: Card):
        self._hand.remove_card(card)

    def hand_size(self):
        return self._hand.size

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def socket(self):
        return self._socket
