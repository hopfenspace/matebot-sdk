import enum
import json
import os
from pprint import pprint

import httpx
import rc_protocol
import staticconfig

import matebot.config


class Http(enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class Network:
    def __init__(self, config: matebot.config.Config):
        self.config = config
        self.client = httpx.AsyncClient(verify=self.config.verify)

    async def make_request(self, verb: Http, address: str, data=None):
        headers = {"Authorization": f"RCP {rc_protocol.get_checksum({}, self.config.secret, salt='/' + address)}"}
        if verb == Http.GET:
            response = await self.client.get(
                os.path.join(self.config.uri, address),
                params=data,
                headers=headers
            )
        elif verb == Http.PUT:
            response = await self.client.put(
                os.path.join(self.config.uri, address),
                json=data,
                headers=headers
            )
        elif verb == Http.DELETE:
            response = await self.client.delete(
                os.path.join(self.config.uri, address),
                headers=headers
            )

        if response.status_code == 200 or response.status_code == 201:
            decoded = json.loads(response.text)
            return decoded
        else:
            try:
                pprint(json.loads(response.text))
            except json.JSONDecodeError:
                print(response.text)
            exit(1)
