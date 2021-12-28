from matebot.objects.base import Base


class Consumable(Base):
    """This class represents a consumable."""
    def __init__(
            self, name: str, price: int, messages: list[str], symbol: str, description: str
    ):
        super(Consumable, self).__init__()
        self.name = name
        self.price = price
        self.messages = messages
        self.symbol = symbol
        self.description = description
