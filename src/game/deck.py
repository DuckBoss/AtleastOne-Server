from collections import deque
from typing import Deque, List, Optional
from random import seed, shuffle, randint
from time import time
from src.game.card import Card


class Deck:
    def __init__(self, max_deck_size=-1, cards: Optional[List[Card]] = None):
        self._cards = deque()
        if max_deck_size == -1:
            self._max_deck_size = 99999
        else:
            self._max_deck_size = max_deck_size
        if cards:
            for card in cards:
                self.add_to_top(card)

    def add_cards(self, cards: [List[Card]]) -> bool:
        if len(cards) > self.size:
            return False
        for card in cards:
            self.add_to_top(card)
        return True

    def add_to_top(self, card: Card) -> bool:
        if self.size < self.max_size:
            self.deck.append(card)
            return True
        return False

    def add_to_bottom(self, card: Card) -> bool:
        if self.size < self.max_size:
            self.deck.appendleft(card)
            return True
        return False

    def draw_random(self) -> Card:
        seed(time())
        deck_list = list(self.deck)
        card = deck_list[randint(0, len(self.deck)-1)]
        self.deck.remove(card)
        return card

    def draw(self) -> Card:
        return self.deck.pop()

    def draw_bottom(self) -> Card:
        return self.deck.popleft()

    def shuffle_deck(self):
        seed(time())
        shuffle(self._cards)

    @property
    def deck(self) -> Deque:
        return self._cards

    @deck.setter
    def deck(self, value: Deque) -> Deque:
        self._cards = value

    @property
    def size(self) -> int:
        return len(self.deck)

    @property
    def max_size(self):
        return self._max_deck_size

    def __str__(self):
        return f"Deck ({','.join(self.deck)}"
