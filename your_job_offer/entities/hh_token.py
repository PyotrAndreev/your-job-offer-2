from dataclasses import dataclass


@dataclass
class HHTokenModel:
    id: int
    login: str
    access: str
    refresh: str

    def __str__(self):
        return f"HH_Token(id={self.id}, login={self.login})"