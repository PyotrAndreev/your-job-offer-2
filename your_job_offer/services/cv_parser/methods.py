from .parser import ResumeParser
from your_job_offer.entities.user import UserModel

parser = ResumeParser()


def parse(path: str) -> UserModel:
    """
    Парсит вакансию
    """
    return parser.parse(path)
