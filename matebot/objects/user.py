from datetime import datetime
from typing import Union

from matebot.objects.base import Base


class User(Base):
    """This class represents a user."""
    def __init__(
            self, modified: int, created: int, internal: bool, identifier: int, active: bool,
            name: str, user_alias_ids: dict[int, str], balance: int, voucher_id: Union[list, None],
            vouched_for: Union[list, None]
    ):
        super().__init__()
        self.identifier = identifier
        self.name = name
        self.active = active
        self.balance = balance
        self.created = datetime.utcfromtimestamp(created)
        self.modified = datetime.utcfromtimestamp(modified)
        self.internal = internal
        self.voucher_id = voucher_id
        self.user_alias_ids = user_alias_ids
        self.vouched_for = vouched_for
