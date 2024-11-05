import pytest
from os import getenv
from your_job_offer.services.cv_parser.parser import ResumeParser
import json

FILE_PATH = "your_job_offer/tests/parser/files/"


@pytest.fixture(scope='module')
def parser_instance() -> ResumeParser:
    parser = ResumeParser()
    return parser


def test_correct(parser_instance):
    user = parser_instance.parse(FILE_PATH + 'resume1.pdf')
    assert user.first_name == "Руслан"
    assert user.last_name == "Яфаров"