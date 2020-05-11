from src.game.deck import Deck


class TestInfiniteDeck:
    def setup_method(self):
        self.random_picked_cards = {}
        self.deck_obj = Deck(infinite_deck=True)

    def teardown_method(self):
        del self.random_picked_cards
        del self.deck_obj

    def test_draw_1000_cards(self):
        for x in range(1000):
            card = self.deck_obj.draw()
            try:
                self.random_picked_cards[card.id] += 1
            except KeyError:
                self.random_picked_cards[card.id] = 1

        counter = 0
        for item in self.random_picked_cards.values():
            counter += item
        assert counter == 1000
