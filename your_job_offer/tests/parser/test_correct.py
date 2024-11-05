import pytest
from your_job_offer.services.cv_parser.parser import ResumeParser
import your_job_offer.services.cv_parser.errors as errors

FILE_PATH = "your_job_offer/tests/parser/files/"


@pytest.fixture(scope="module")
def parser_instance() -> ResumeParser:
    parser = ResumeParser()
    return parser


def test_correct(parser_instance):
    user = parser_instance.parse(FILE_PATH + "resume1.pdf")
    assert user.first_name == "Руслан"
    assert user.last_name == "Яфаров"


def test_image(parser_instance):
    user = parser_instance.parse(FILE_PATH + "resume_with_photo.pdf")
    assert user.first_name == "Janine"
    assert user.last_name == "Nel"


def test_too_big_file(parser_instance):
    try:
        parser_instance.parse(FILE_PATH + "too_big_file.pdf")
    except ValueError as e:
        assert e == errors.TooBigFile


def test_not_pdf(parser_instance):
    try:
        parser_instance.parse(FILE_PATH + "resume_docx.docx")
    except ValueError as e:
        assert e == errors.NotPdf
