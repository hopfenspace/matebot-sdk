from datetime import datetime

from matebot.objects.base import Base


class Communism(Base):
    """This class represents a communism."""
    def __init__(self, active: bool, identifier: int, amount: int, reason: str, creator_id: int,
                 participant_ids: list[int], created: float, modified: float):
        super().__init__()
        self.active = active
        self.identifier = identifier
        self.amount = amount
        self.reason = reason
        self.creator_id = creator_id
        self.participant_ids = participant_ids
        self.created = datetime.utcfromtimestamp(created)
        self.modified = datetime.utcfromtimestamp(modified)


