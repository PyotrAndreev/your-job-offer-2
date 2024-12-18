import re
import json
from os import getenv
from typing import Optional, Any

import pdftotext
from openai import OpenAI

from .tokenizer import num_tokens_from_string

import your_job_offer.entities.user as user_models
import your_job_offer.services.cv_parser.errors as errors
from your_job_offer.logger import get_logger

log = get_logger(__name__)


class OpenaAIQueryBuilder:
    def __init__(self, PROXY_API_KEY: str, model: str = "gpt-4o-mini"):
        self.PROXY_API_KEY = PROXY_API_KEY
        self.model = model
        self.client = OpenAI(
            api_key=f"{PROXY_API_KEY}",
            base_url="https://api.proxyapi.ru/openai/v1",
        )

    def query(self, content: str, max_tokens: int = 1000) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": content}],
                max_tokens=max_tokens,
            )
        
            return response.choices[0].message.content
        except Exception:
            log.info("деньги закончились(")


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
  "gender": один из вариантов "male" "female",
  "phone": возможно +, затем цифры без пробелов и скобок,
  "email": "",
  "country": "",
  "city": "",
  "country": "",
  "cv": url,
  "description": "",
  "work_type": один из вариантов "office" "remote" "hybrid" "field_work",
  "min_salary": "",
  "max_salary": "",
  "business_trip_readiness": один из вариантов "ready" "sometimes" "never",
  "relocation": один из вариантов "no_relocation" "relocation_possible" "relocation_desirable",
  "education": один из вариантов "secondary" "special_secondary" "unfinished_higher" "higher" "bachelor" "master" "candidate" "doctor",
  "employment": один из вариантов "full" "part" "project" "volunteer" "probation",
  "schedule": один из вариантов "fullDay" "shift" "flexible" "remote" "flyInFlyOut",
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
    {
      "name": "",
      "description": ""
    }
  ],
  "educations": [
    {
        "institution": "",
        "major": "",
        "degree": "",
        "description": ""
        "start_date": "",
        "finish_date": ""
    }
  ],
  "languages": [
    {
        "name": "",
        "level": один из вариантов "a1" "a2" "b1" "b2" "c1" "c2" "l1",
    }
  ]
}

Даты указывай в формате year-month-day
Не добавляй никакого дополнительного текста перед или после JSON.
"""
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
        if response is None:
            return {}
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
        try:
            result_dict = self.parser.parse(pdf_path)
            return ResumeParser._dict_to_user(result_dict)
        except Exception:
            log.exception("что-то пошло не так: ")
            return user_models.UserModel()

    @staticmethod
    def _field_to_class(field: str, cls=str) -> Optional[Any]:
        if len(field) == 0:
            return None
        try:
            ans = cls(field)
        except ValueError:
            return None
        return ans

    @staticmethod
    def _field_to_int(field: str) -> Optional[int]:
        return ResumeParser._field_to_class(field, int)

    @staticmethod
    def _dict_to_user(user: dict) -> user_models.UserModel:
        if user == {}:
            return user_models.UserModel()
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
        skills = [user_models.SkillModel(**skill) for skill in user["skills"]]
        educations = [
            user_models.EducationModel(**education)
            for education in user["educations"]
        ]
        city = (
            user_models.CityModel(name=user["city"])
            if user["city"] != ""
            else None
        )
        country = (
            user_models.CountryModel(name=user["country"])
            if user["country"] != ""
            else None
        )
        languages = [
            user_models.LanguageModel(
                name=language["name"],
                level=ResumeParser._field_to_class(
                    language["level"], user_models.LanguageLevelEnum
                ),
            )
            for language in user["languages"]
        ]
        return user_models.UserModel(
            birth_date=ResumeParser._field_to_class(user["birth_date"]),
            first_name=ResumeParser._field_to_class(user["first_name"]),
            last_name=ResumeParser._field_to_class(user["last_name"]),
            middle_name=ResumeParser._field_to_class(user["middle_name"]),
            gender=ResumeParser._field_to_class(
                user["gender"], user_models.GenderEnum
            ),
            phone=ResumeParser._field_to_class(user["phone"]),
            email=ResumeParser._field_to_class(user["email"]),
            city=city,
            country=country,
            cv=ResumeParser._field_to_class(user["cv"]),
            description=ResumeParser._field_to_class(user["description"]),
            work_type=ResumeParser._field_to_class(
                user["work_type"], user_models.WorkTypeEnum
            ),
            min_salary=ResumeParser._field_to_int(user["min_salary"]),
            max_salary=ResumeParser._field_to_int(user["max_salary"]),
            business_trip_readiness=ResumeParser._field_to_class(
                user["business_trip_readiness"],
                user_models.BusinessTripReadinessEnum,
            ),
            relocation=ResumeParser._field_to_class(
                user["relocation"], user_models.RelocationEnum
            ),
            employment=ResumeParser._field_to_class(
                user["employment"], user_models.EmploymentEnum
            ),
            schedule=ResumeParser._field_to_class(
                user["schedule"], user_models.ScheduleEnum
            ),
            education_level=ResumeParser._field_to_class(
                user["education"], user_models.EducationLevelEnum
            ),
            projects=projects,
            achievements=achievements,
            work_experiences=work_experience,
            educations=educations,
            skills=skills,
            languages=languages,
        )
