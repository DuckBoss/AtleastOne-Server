from collections import deque
from typing import Deque, List, Optional
from random import seed, shuffle, randint, random
from time import time
from src.game.card import Card
from copy import deepcopy


class Deck:
    def __init__(self, infinite_deck: bool = False, players_per_deck=10, cards: Optional[List[Card]] = None):
        self._cards = deque()
        self.infinite_deck = infinite_deck
        self.players_per_deck = players_per_deck
        if infinite_deck:
            from src.game.utils.deck_utils import generate_card_dictionary
            self.card_dictionary = generate_card_dictionary()
            return
        if cards:
            self.add_cards(cards)
            self.shuffle_deck()

    def generate_default_deck(self, card_definitions_file, num_of_players):
        self._cards = deque()
        self.infinite_deck = False
        import json
        from math import ceil
        json_path = card_definitions_file
        with open(json_path, 'r') as card_defs:
            data = json.load(card_defs)
            # Retrieve all cards
            for card_color in data['cards']['colors']:
                print(f"{card_color} - "
                      f"\n{data['cards']['colors'][card_color]['values']}")
                for card_value in data['cards']['colors'][card_color]['values']:
                    self.add_to_top(Card(card_color=card_color, card_value=card_value,
                                         card_hex=data['cards']['colors'][card_color]['hex']))
        self.deck = ceil(num_of_players / float(self.players_per_deck)) * self.deck
        self.shuffle_deck()

    def get_top_card(self):
        return self._cards[-1]

    def add_cards(self, cards: [List[Card]]) -> bool:
        for card in cards:
            self.add_to_top(card)

    def add_to_top(self, card: Card) -> bool:
        self.deck.append(card)

    def add_to_bottom(self, card: Card) -> bool:
        self.deck.appendleft(card)

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

    def remove_card(self, card: Card) -> bool:
        if self.infinite_deck:
            return False
        return self.deck.remove(card)

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

    def __str__(self):
        if self.infinite_deck:
            return f"Deck (Infinite Size)"
        return f"Deck ({','.join(self.deck)}"
