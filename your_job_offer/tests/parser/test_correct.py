import pytest
from  services.cv_parser.methods import parse
import  services.cv_parser.errors as errors

FILE_PATH = "your_job_offer/tests/parser/files/"


def test_correct():
    user = parse(FILE_PATH + "resume1.pdf")
    assert user.first_name == "Руслан"
    assert user.last_name == "Яфаров"


def test_image():
    user = parse(FILE_PATH + "resume_with_photo.pdf")
    assert user.first_name == "Janine"
    assert user.last_name == "Nel"


def test_too_big_file():
    with pytest.raises(errors.TooBigFile):
        parse(FILE_PATH + "too_big_file.pdf")


def test_not_pdf():
    with pytest.raises(errors.NotPdf):
        parse(FILE_PATH + "resume_docx.docx")
