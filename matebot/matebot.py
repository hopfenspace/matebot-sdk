from os.path import join
from typing import List, Any, Union

from matebot.config import Config
from matebot.networking import Network, Http
from matebot.objects.consumable import Consumable
from matebot.objects.transaction import Transaction
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

    async def get_consumables(self) -> list[Union[Consumable, None]]:
        """This method is used to get the list of Consumables

        :return: List of Consumables or empty list
        """
        res = await self.network.make_request(Http.GET, "api/v1/getConsumables")
        return [Consumable(**x) for x in res["data"]]

    async def get_user(self, user_id: int = None) -> Union[None, list[Any], list[User], User]:
        """This method is used to retrieve user(s)

        :param user_id: Optional. Queries only the specified user.
        :return: List of Users or single User
        """
        data = {}
        if user_id:
            data["filter"] = user_id
        res = await self.network.make_request(Http.GET, "api/v1/getUser", data=data)
        if not res:
            return
        if not res["data"]:
            return None if user_id else []
        if isinstance(res["data"], list):
            return [User(**x) for x in res["data"]]
        return User(**res["data"])

    async def create_user(self, user_alias: str, name: str = None) -> int:
        """This method is used to create a user

        :param user_alias: Identifier of the application.
        :param name: Optional. Name of the user
        :return: Returns the ID of the newly created User
        """
        data = {
            "user_alias": user_alias,
            "application_id": self.config.application_id
        }
        if name:
            data["name"] = name
        res = await self.network.make_request(Http.POST, "api/v1/createUser", data=data)
        return int(res["data"])

    async def perform_transaction(self, sender_id: int, receiver_id: int, amount: int, reason: str) -> int:
        """This method is used to perform a transaction

        :param sender_id: ID of the sender
        :param receiver_id: ID of the receiver
        :param amount: Positive amount to send
        :param reason: Reason for history

        :return: Returns the ID of the transaction
        """
        data = {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "amount": amount,
            "reason": reason
        }
        res = await self.network.make_request(Http.POST, "api/v1/performTransaction", data=data)
        return int(res["data"])

    async def get_history(self, target_id: int, amount: int = None) -> list[Transaction]:
        """This method is used to retrieve the history of a target.

        :param target_id: ID of the target
        :param amount: Optional. Amount of transactions to retrieve.

        :return: Returns a list of the retrieved transactions
        """
        data = {
            "target_id": target_id
        }
        if amount:
            data["amount"] = amount
        res = await self.network.make_request(Http.GET, "api/v1/getHistory", data=data)
        return [Transaction(**x) for x in res["data"]]

    async def del_user_alias(self, user_id: int, application_id: int) -> bool:
        """This method is used to delete a user alias

        :param user_id: ID of the user alias
        :param application_id: ID of the application

        :return: Returns a bool if the operation was executed successfully
        """
        data = {
            "user_id": user_id,
            "application_id": application_id
        }
        res = await self.network.make_request(Http.POST, "api/v1/deleteUserAlias", data=data)
        return res["success"]

    async def start_vouch(self, user_id, target_id) -> bool:
        """This method is used to start vouching for another user

        :param user_id: ID of the vouching user
        :param target_id: ID of the user that is vouched for

        :return: Returns True if the operation was successful
        """
        data = {
            "user_id": user_id,
            "target_id": target_id
        }
        res = await self.network.make_request(Http.POST, "api/v1/startVouch", data=data)
        if not res["success"]:
            print(res["info"])
        return res["success"]

    async def end_vouch(self, user_id, target_id) -> bool:
        """This method is used to stop vouching for a user

        :param user_id: ID of the vouching user
        :param target_id: ID of the user that is vouched for

        :return: True if the operation was successful
        """
        data = {
            "user_id": user_id,
            "target_id": target_id
        }
        res = await self.network.make_request(Http.POST, "api/v1/endVouch", data=data)
        if not res["success"]:
            print(res["info"])
        return res["success"]

    async def start_refund(self, user_id: int, amount: int, reason: str = None) -> int:
        """This method is used to start a refund process for a specific user

        :param user_id: ID of the user
        :param amount: Amount of the refund
        :param reason: Optional. Reason of the refund

        :return: ID of the refund
        """
        data = {
            "user_id": user_id,
            "amount": amount,
        }
        if reason:
            data["reason"] = reason
        res = await self.network.make_request(Http.POST, "api/v1/startRefund", data=data)
        if not res["success"]:
            print(res["info"])
        return res["data"]

    async def cancel_refund(self, refund_id: int) -> bool:
        """This method is used to cancel a refund

        :param refund_id: ID of the refund
        :return: Returns True if the refund was canceled
        """
        data = {
            "refund_id": refund_id
        }
        res = await self.network.make_request(Http.POST, "api/v1/cancelRefund", data=data)
        if not res["success"]:
            print(res["info"])
        return res["success"]

    async def vote_refund(self, user_id: int, refund_id: int, positive: bool) -> bool:
        """This method is used to vote for a refund

        :param user_id: ID of the user that wants to vote
        :param refund_id: ID of the refund
        :param positive: Vote bool

        :return: Returns True if the vote action was successful
        """
        data = {
            "user_id": user_id,
            "refund_id": refund_id,
            "positive": positive
        }
        res = await self.network.make_request(Http.POST, "api/v1/voteRefund", data=data)
        return res["success"]

    async def retract_refund_vote(self, user_id: int, refund_id: int) -> bool:
        """This method is used to retract the vote from a refund request

        :param user_id: ID of the user the vote originated
        :param refund_id: ID of the refund
        :return: Returns True if the operation was successful
        """
        data = {
            "user_id": user_id,
            "refund_id": refund_id
        }
        res = await self.network.make_request(Http.POST, "api/v1/retractRefundVote", data=data)
        return res["success"]