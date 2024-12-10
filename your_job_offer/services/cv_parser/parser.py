import re
import json
from os import getenv
from typing import Optional

import pdftotext
from openai import OpenAI

from .tokenizer import num_tokens_from_string

import  entities.user as user_models
import  services.cv_parser.errors as errors
from  logger import get_logger

log = get_logger(__name__)


class OpenaAIQueryBuilder:
    def __init__(self, PROXY_API_KEY: str, model: str = "gpt-4o-mini"):
        self.PROXY_API_KEY = PROXY_API_KEY
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
    return pdf_str


class _ResumeParser:
    PRICES = {
        "gpt-4o-mini": {
            "request_per_thousand_token_price": 0.0432,
            "response_per_thousand_token_price": 0.1728,
        }
    }

    def __init__(
        self,
        OPENAI_API_KEY: str,
        max_tokens: int = 5000,
        model: str = "gpt-4o-mini",
    ):
        self.prompt_questions = """
Пожалуйста, резюмируй текст ниже в формате JSON без лишних строк текста.
Вот структура, которой ты должен следовать:

{
  "birth_date": "",
  "first_name": "",
  "last_name": "",
  "middle_name": "",
  "gender": "",
  "phone": возможно +, затем цифры без пробелов и скобок,
  "email": "",
  "country": "",
  "city": "",
  "country": "",
  "cv": url,
  "description": "",
  "work_type": "",
  "min_salary": "",
  "max_salary": "",
  "business_trip_readiness": 0 or 1,
  "work_hours": "",
  "relocation": 0 or 1,
  "education": один из вариантов "secondary" "special_secondary" "unfinished_higher" "higher" "bachelor" "master" "candidate" "doctor",
  "project_experience": [
    {
      "name": "",
      "description": "",
      "link": ""
    }
  ],
  "achievements": [
    {
      "name": "",
      "description: "",
      "link": ""
    },
  ]
  "work_experiences": [
    {
      "job": "",
      "work_place": "",
      "description": "",
      "start_date": "",
      "finish_date": ""
    }
  ],
  "skills": [
    ""
  ]
}

Даты указывай в формате year-month-day
Не добавляй никакого дополнительного текста перед или после JSON.
"""  # TODO запрос
        self.query_builder = OpenaAIQueryBuilder(OPENAI_API_KEY)
        self.max_tokens = max_tokens
        self.model = model

    def parse(self, pdf_path: str) -> dict:
        """
        Делает запрос gpt в виде текста pdfки для извлечения информации
        :param pdf_path: Path to the PDF file.
        :return dictionary of resume with keys (basic_info, work_experience).
        """
        try:
            pdf_str = pdf2string(pdf_path)
        except pdftotext.Error:
            raise errors.NotPdf

        prompt = self.prompt_questions + "\n" + pdf_str
        estimated_prompt_tokens = num_tokens_from_string(prompt, self.model)
        max_answer_tokens = self.max_tokens - estimated_prompt_tokens
        if max_answer_tokens < 0:
            self._too_big_file_error(estimated_prompt_tokens)
        response = self.query_builder.query(
            prompt, max_tokens=max_answer_tokens
        )
        tokens_answer_count = num_tokens_from_string(response, self.model)
        if tokens_answer_count == max_answer_tokens:
            self._too_big_file_error(estimated_prompt_tokens)
        log.info(
            f"Запрос отработан, на запросе {estimated_prompt_tokens}, \
            на ответе {tokens_answer_count} токенов, \
            всего на запрос затрачено \
            {self._calculate_cost(estimated_prompt_tokens, tokens_answer_count)} рублей"
        )
        resume = json.loads(response)
        return resume

    def _too_big_file_error(self, estimated_prompt_tokens: int) -> None:
        log.info(f"Слишком большой файл, {estimated_prompt_tokens} токенов")
        raise errors.TooBigFile

    def _calculate_cost(
        self, estimated_prompt_tokens: int, tokens_answer_count: int
    ) -> float:
        """Считает сколько примерно стоил запрос"""
        return (
            self.PRICES[self.model]["request_per_thousand_token_price"]
            * estimated_prompt_tokens
            + self.PRICES[self.model]["response_per_thousand_token_price"]
            * tokens_answer_count
        ) / 1000


class ResumeParser:
    def __init__(self):
        openai_api_key = getenv("OPENAI_API_KEY")
        if openai_api_key is None:
            log.error("OPENAI_API_KEY не найден.")
            raise KeyError(
                "OPENAI_API_KEY не найден. \
                Убедись, что запускал build.sh \
                и есть файл .env c ключём"
            )
        self.parser = _ResumeParser(openai_api_key)

    def parse(self, pdf_path: str) -> user_models.UserModel:
        result_dict = self.parser.parse(pdf_path)
        return ResumeParser._dict_to_user(result_dict)

    @staticmethod
    def _field_to_int(field: str) -> Optional[int]:
        if len(field) == 0:
            return None
        return int(field)

    @staticmethod
    def _field_to_str(field: str) -> Optional[str]:
        if len(field) == 0:
            return None
        return field

    @staticmethod
    def _dict_to_user(user: dict) -> user_models.UserModel:
        projects = [
            user_models.ProjectModel(**project)
            for project in user["project_experience"]
        ]
        work_experience = [
            user_models.WorkExperienceModel(**work_experience)
            for work_experience in user["work_experiences"]
        ]
        achievements = [
            user_models.AchievementModel(**achievement)
            for achievement in user["achievements"]
        ]
        education_level = (
            user_models.EducationLevelEnum(user["education"])
            if user["education"] != ""
            else None
        )

        return user_models.UserModel(
            birth_date=ResumeParser._field_to_str(user["birth_date"]),
            first_name=user_models.Name(user["first_name"]),
            last_name=user_models.Name(user["last_name"]),
            middle_name=user_models.Name(user["middle_name"]),
            gender=user["gender"],
            phone=ResumeParser._field_to_str(user["phone"]),
            email=ResumeParser._field_to_str(user["email"]),
            city=user["city"],
            country=user["country"],
            cv=user["cv"],
            description=user["description"],
            work_type=user["work_type"],
            education_level=education_level,
            min_salary=ResumeParser._field_to_int(user["min_salary"]),
            max_salary=ResumeParser._field_to_int(user["max_salary"]),
            business_trip_readiness=user["business_trip_readiness"],
            work_hours=ResumeParser._field_to_int(user["work_hours"]),
            relocation=user["relocation"],
            projects=projects,
            skills=user["skills"],
            work_experiences=work_experience,
            achievements=achievements,
        )
