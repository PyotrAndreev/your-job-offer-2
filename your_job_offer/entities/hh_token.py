from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class HHTokenModel:
    id: int
    login: str
    access_token: str
    refresh_token: str

    def __str__(self):
        return f"HH_Token(id={self.id}, login={self.login})"