import json
from dataclasses import dataclass, field
from json import JSONDecodeError
from typing import Any

from exceptions.server_exceptions import WrongRequestData


JSONLike = dict | list[dict]


@dataclass
class Response:
    """The response which is returned by handler."""
    data: JSONLike


@dataclass
class Request:
    """
    The abstraction of websocket connection. Represents useful data
    which may be used in handlers.
    """
    raw_data: Any
    data: dict = field(init=False)

    def __post_init__(self):
        """
        Creates from the raw data (actually string) a dict and saves it.
        """
        self.data = self.construct_json_data(self.raw_data)

    @staticmethod
    def construct_json_data(data: str) -> dict:
        """Constructs from a string a JSON object (dict)."""
        try:
            deserialized_data = json.loads(data)
        except (JSONDecodeError, TypeError) as e:
            raise WrongRequestData(repr(e))
        else:
            if not isinstance(deserialized_data, dict):
                raise WrongRequestData("The request data must be in the JSON format.")
        return deserialized_data
