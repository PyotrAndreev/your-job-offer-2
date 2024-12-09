import logging
from os import getenv
import json

from your_job_offer.services.cv_parser.parser import OpenaAIQueryBuilder
from your_job_offer.services.cv_parser.tokenizer import num_tokens_from_string
from your_job_offer.entities.user import EmailMessage
from your_job_offer.entities.tracking import (
    ParsedMessage,
    VacancyKey,
    Stage,
    StageEnum,
)


class EmailParser:
    PRICES = {
        "gpt-4o-mini": {
            "request_per_thousand_token_price": 0.0432,
            "response_per_thousand_token_price": 0.1728,
        }
    }

    def __init__(
        self,
        max_tokens_for_message: int = 1000,
        max_summary_tokens: int = 16384,
        model: str = "gpt-4o-mini",
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            f"your_job_offer/logs/{__name__}.log", mode="w"
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        )
        self.logger.addHandler(handler)
        openai_api_key = getenv("OPENAI_API_KEY")
        if openai_api_key is None:
            self.logger.error("OPENAI_API_KEY не найден.")
            raise KeyError(
                "OPENAI_API_KEY не найден. \
                Убедись, что запускал build.sh \
                и есть файл .env c ключём"
            )
        self.query_builder = OpenaAIQueryBuilder(openai_api_key)
        self.max_tokens_for_message = max_tokens_for_message
        self.max_summary_tokens = max_summary_tokens
        self.model = model
        self.prompt_questions = """
Из каждого сообщения выдели нужную информацию:
Вот структура, который ты должен придерживаться.

{
"ans":
    [
    {
        "job": "",
        "employer": "",
        "stage": строка, одно из 4 "consideration", "reject", "invite"(это значит нужно заполнить какую-то информацию или записаться на собеседование), "testing", "interview"(этап invite пройден, нужно записаться на собеседование)
        "deadline": время, до которого нужно что-то сделать,
    }
    ]
}

Сообщения начинаются с <message> и заканчиваются на <message>
Не надо ничего переводить, если сообщения и данные на английском - пусть остаются на английском
Если же хотя бы одного "job" или "employer" нет, то в списке этот элемент сделай ""(но ни в ком случае не пропускай его! в ответном json должно оказаться ровно столько же элементов, сколько было сообщений во входе). Даты указывай в формате year-month-day
Не добавляй никакого дополнительного текста перед или после JSON.\n
"""

    def parse(
        self, messages: list[EmailMessage]
    ) -> list[ParsedMessage | None]:
        result: list[ParsedMessage | None] = [None] * len(messages)
        nones: list[int] = []
        prompt = self.prompt_questions
        for index, message in enumerate(messages):
            if (
                num_tokens_from_string(message.body, self.model)
                > self.max_tokens_for_message
            ):
                nones.append(index)
            else:
                prompt += "<message>" + message.body + "<message>\n"
        estimated_prompt_tokens = num_tokens_from_string(prompt, self.model)
        max_answer_tokens = self.max_summary_tokens - estimated_prompt_tokens
        if max_answer_tokens < 0:
            raise RuntimeError(
                "бро пришло слишком много писем, нам это не по-карману"
            )
        response = self.query_builder.query(
            prompt, max_tokens=max_answer_tokens
        )
        tokens_answer_count = num_tokens_from_string(response, self.model)
        if tokens_answer_count == max_answer_tokens:
            raise RuntimeError(
                "бро пришло слишком много писем, нам это не по-карману"
            )
        self.logger.info(
            f"Запрос отработан, на запросе {estimated_prompt_tokens}, \
            на ответе {tokens_answer_count} токенов, \
            всего на запрос затрачено \
            {self._calculate_cost(estimated_prompt_tokens, tokens_answer_count)} рублей"
        )
        resume = json.loads(response)["ans"]
        nones_count = 0
        for i in range(len(messages)):
            info = resume[i - nones_count]
            if nones_count < len(nones) and nones[nones_count] == i:
                nones_count += 1
            elif not (
                info["job"] == ""
                or info["employer"] == ""
                or info["stage"] == ""
            ):
                result[i] = self._info_to_parsed_message(info)
        return result

    @staticmethod
    def _info_to_parsed_message(info: dict[str, str]):
        return ParsedMessage(
            VacancyKey(job=info["job"], employer=info["employer"]),
            Stage(
                stage_type=StageEnum(info["stage"]), deadline=info["deadline"]
            ),
        )

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


parser = EmailParser()
