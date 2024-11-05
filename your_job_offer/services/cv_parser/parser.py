import re
import json
from os import getenv
import logging

import pdftotext
from openai import OpenAI

from .tokenizer import num_tokens_from_string
import your_job_offer.services.cv_parser.errors as errors
from your_job_offer.domain.models.user import User


class OpenaAIQueryBuilder:
    def __init__(self, PROXY_API_KEY: str, model: str = "gpt-4o-mini"):
        self.PROXY_API_KEY: str = PROXY_API_KEY
        self.model = model
        self.client = OpenAI(
            api_key=f"{PROXY_API_KEY}",
            base_url="https://api.proxyapi.ru/openai/v1",
        )

    def query(self, content: str, max_tokens: int = 1000) -> str | None:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


def pdf2string(pdf_path: str) -> str:
    """
    Получает строку по pdf
    :param pdf_path: Путь
    :return: строка всего контента pdf
    """
    with open(pdf_path, "rb") as f:
        pdf = pdftotext.PDF(f)
    pdf_str = "\n\n".join(pdf)
    pdf_str = re.sub(r"\s[,.]", ",", pdf_str)
    pdf_str = re.sub("[\n]+", "\n", pdf_str)
    pdf_str = re.sub(r"[\s]+", " ", pdf_str)
    # pdf_str = re.sub("http[s]?(://)?", "", pdf_str)
    return pdf_str


class _ResumeParser:
    def __init__(
        self,
        OPENAI_API_KEY: str,
        max_tokens: int = 5000,
        model: str = "gpt-4o-mini",
    ):
        self.prompt_questions = """
Пожалуйста, резюмируй текст ниже в формате JSON без лишних строк текста. Вот структура, которой ты должен следовать:

{
  "birth_date": "",
  "first_name": "",
  "last_name": "",
  "middle_name": "",
  "gender": "",
  "phone": "",
  "email": "",
  "country": "",
  "city": "",
  "country": "",
  "cv": url,
  "description": "",
  "work_type": "",
  "min_salary": "",
  "max_salary": "",
  "buisiness_trip_readiness": 0 or 1,
  "work_hours": "",
  "relocation": 0 or 1,
  "project_experience": [
    {
      "title": "",
      "description": "",
      "link": ""
    }
  ],
  "achievements": [
    {
      "title": "",
      "description: "",
      "link": ""
    },
  ]
  "work_experience": [
    {
      "job_title": "",
      "company": "",
      "location": "",
      "duration": "",
      "job_summary": ""
    }
  ],
}

Не добавляй никакого дополнительного текста перед или после JSON.
"""  # TODO запрос
        self.query_builder = OpenaAIQueryBuilder(OPENAI_API_KEY)
        self.max_tokens = max_tokens
        self.model = model

        self.logger = logging.getLogger(__name__)

    def parse(self, pdf_path: str) -> dict:
        """
        Делает запрос gpt в виде текста pdfки для извлечения информации
        :param pdf_path: Path to the PDF file.
        :return dictionary of resume with keys (basic_info, work_experience).
        """
        try:
            pdf_str = pdf2string(pdf_path)
        except pdftotext.Error as e:
            raise errors.NotPdf

        prompt = self.prompt_questions + "\n" + pdf_str
        estimated_prompt_tokens = num_tokens_from_string(prompt, self.model)
        max_answer_tokens = self.max_tokens - estimated_prompt_tokens
        if max_answer_tokens < 0:
            self._too_big_file_error(estimated_prompt_tokens)
        response = self.query_builder.query(prompt, max_tokens=max_answer_tokens)
        tokens_answer_count = num_tokens_from_string(response, self.model)
        if tokens_answer_count == max_answer_tokens:
            self._too_big_file_error(estimated_prompt_tokens)
        self.logger.info(
            f"Запрос отработан, на запросе {estimated_prompt_tokens}, на ответе {tokens_answer_count} токенов, всего на запрос затрачено {(0.0432 * estimated_prompt_tokens + 0.1728 * tokens_answer_count) / 1000} рублей"
        )
        resume = json.loads(response)
        return resume
    
    def _too_big_file_error(self, estimated_prompt_tokens: int) -> None:
        self.logger.info(f"Слишком большой файл, {estimated_prompt_tokens} токенов")
        raise errors.TooBigFile


class ResumeParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(f"your_job_offer/logs/{__name__}.log", mode="w")
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        )
        self.logger.addHandler(handler)
        openai_api_key = getenv("OPENAI_API_KEY")
        if openai_api_key is None:
            self.logger.error("OPENAI_API_KEY не найден.")
            raise KeyError(
                "OPENAI_API_KEY не найден. Убедись, что запускал build.sh и есть файл .env c ключём"
            )
        self.parser = _ResumeParser(openai_api_key)

    def parse(self, pdf_path: str) -> User:
        result_dict: dict = self.parser.parse(pdf_path)
        return ResumeParser._dict_to_user(result_dict)

    @staticmethod
    def _dict_to_user(user: dict) -> User:
        return User(user.get("first_name"), user.get("last_name"))
