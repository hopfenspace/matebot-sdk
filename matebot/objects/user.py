from datetime import datetime
from typing import Union

from matebot.objects.base import Base


class User(Base):
    """This class represents a user."""
    def __init__(
            self, modified: int, created: int, complete_access: bool, external: bool, identifier: int, active: bool,
            name: str, user_alias_ids: list, balance: int, voucher_id: Union[list, None]
    ):
        super().__init__()
        self.identifier = identifier
        self.name = name
        self.complete_access = complete_access
        self.active = active
        self.balance = balance
        self.created = datetime.utcfromtimestamp(created)
        self.modified = datetime.utcfromtimestamp(modified)
        self.external = external
        self.voucher_id = voucher_id
        self.user_alias_ids = user_alias_ids
