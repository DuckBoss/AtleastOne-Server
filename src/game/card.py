class Card:
    def __init__(self, card_color: str, card_category: str, card_number: int = -1, card_hex: str = ''):
        self.number = int(card_number)
        self.color = card_color
        self.category = card_category
        self.hex = card_hex
        self.generate_id()

    def generate_id(self):
        self.id = f"{self.category[0]}{abs(self.number)}"

    def get_json(self):
        return {
            'id': self.id,
            'type': self.category,
            'color': self.color,
            'number': self.number,
            'hex': self.hex
        }

    def get_json_dump(self):
        from json import dumps
        return dumps(self.get_json())

    def __str__(self):
        return f"Card (ID - {self.id}, Number - {self.number}, Color = {self.color}, Type - {self.category}, Hex - {self.hex})"
