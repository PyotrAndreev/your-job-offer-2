from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class HHTokenModel:
    """
    Represents a model for storing the HH (HeadHunter) API token details.

    Attributes:
        id (int): The unique identifier of the token.
        login (str): The login associated with the token.
        access_token (str): The access token used for authentication with the HH API.
        refresh_token (str): The refresh token used to renew the access token.

    Methods:
        __str__: Returns a string representation of the HHTokenModel instance, displaying the token's ID and login.
    """
    id: int
    login: str
    access_token: str
    refresh_token: str

    def __str__(self):
        return f"HH_Token(id={self.id}, login={self.login})"
