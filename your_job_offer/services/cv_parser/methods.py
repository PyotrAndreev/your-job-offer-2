from .parser import ResumeParser
from  entities.user import UserModel

parser = ResumeParser()


def parse(path: str) -> UserModel:
    """
    Парсит вакансию
    """
    return parser.parse(path)
