from os.path import join
from typing import List, Any, Union

from matebot.config import Config
from matebot.networking import Network, Http
from matebot.objects.consumable import Consumable
from matebot.objects.user import User


class MateBot:
    def __init__(self, config_path=None):
        if config_path:
            self.config = Config.from_json(config_path)
        else:
            self.config = Config.from_json("config.json")
        self.network = Network(self.config)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.network.client.aclose()

    async def get_consumables(self):
        res = await self.network.make_request(Http.GET, "api/v1/getConsumables")
        return [Consumable(**x) for x in res["data"]]

    async def get_user(self, user_id: int = None) -> Union[None, list[Any], list[User], User]:
        """This method is used to retrieve user(s)

        :param user_id: Optional. Queries only the specified user.
        :return: List of Users or single User
        """
        res = await self.network.make_request(Http.GET, "api/v1/getUser", data={"filter": user_id})
        if not res:
            return
        if not res["data"]:
            return None if user_id else []
        if isinstance(res["data"], list):
            return [User(**x) for x in res["data"]]
        return User(**res["data"])
