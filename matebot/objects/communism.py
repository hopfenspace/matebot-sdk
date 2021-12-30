from datetime import datetime

from matebot.objects.base import Base


class Communism(Base):
    """This class represents a communism."""
    def __init__(self, active: bool, identifier: int, amount: int, reason: str, creator_id: int,
                 participants: list[dict], created: float, modified: float):
        super().__init__()
        self.active = active
        self.identifier = identifier
        self.amount = amount
        self.reason = reason
        self.creator_id = creator_id
        self.participants = participants
        self.created = datetime.utcfromtimestamp(created)
        self.modified = datetime.utcfromtimestamp(modified)


