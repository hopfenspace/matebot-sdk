from datetime import datetime

from matebot.objects.base import Base


class Transaction(Base):
    """This class represents a transaction"""
    def __init__(self, sender_id: int, receiver_id: int, amount: int, reason: str, created: float):
        super(Transaction, self).__init__()
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.reason = reason
        self.created = datetime.utcfromtimestamp(created)

