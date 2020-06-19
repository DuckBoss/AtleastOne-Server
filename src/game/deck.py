from collections import deque
from typing import Deque, List, Optional
from random import seed, shuffle, randint, random
from time import time
from src.game.card import Card
from copy import deepcopy


class Deck:
    def __init__(self, infinite_deck: bool = False, max_deck_size=-1, cards: Optional[List[Card]] = None):
        self._cards = deque()
        self.infinite_deck = infinite_deck
        if infinite_deck:
            from src.game.utils.deck_utils import generate_card_dictionary
            self.card_dictionary = generate_card_dictionary()
            self._max_deck_size = 99999
            return
        if max_deck_size == -1:
            self._max_deck_size = 99999
        else:
            self._max_deck_size = max_deck_size
        if cards:
            self._max_deck_size = len(cards)
            self.add_cards(cards)
            self.shuffle_deck()

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
        if self.infinite_deck:
            seed(random())
            picked_card_index = randint(0, len(self.card_dictionary)-1)
            picked_card = deepcopy(self.card_dictionary[picked_card_index])
            return picked_card
        return self.deck.pop()

    def draw_bottom(self) -> Card:
        if self.infinite_deck:
            return self.draw()
        return self.deck.popleft()

    def shuffle_deck(self):
        if self.infinite_deck:
            return
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
        if self.infinite_deck:
            return f"Deck (Infinite Size)"
        return f"Deck ({','.join(self.deck)}"
