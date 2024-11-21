import pytest
from your_job_offer.services.cv_parser.parser import ResumeParser
import your_job_offer.services.cv_parser.errors as errors

FILE_PATH = "your_job_offer/tests/parser/files/"


@pytest.fixture(scope="module")
def parser() -> ResumeParser:
    parser_instance = ResumeParser()
    return parser_instance


def test_correct(parser: ResumeParser):
    user = parser.parse(FILE_PATH + "resume1.pdf")
    assert user.first_name == "Руслан"
    assert user.last_name == "Яфаров"


def test_image(parser: ResumeParser):
    user = parser.parse(FILE_PATH + "resume_with_photo.pdf")
    assert user.first_name == "Janine"
    assert user.last_name == "Nel"


def test_too_big_file(parser: ResumeParser):
    with pytest.raises(errors.TooBigFile):
        parser.parse(FILE_PATH + "too_big_file.pdf")


def test_not_pdf(parser: ResumeParser):
    with pytest.raises(errors.NotPdf):
        parser.parse(FILE_PATH + "resume_docx.docx")
