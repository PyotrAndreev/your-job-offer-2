import requests

import your_job_offer.logger as logger

log = logger.get_logger(__name__)


def apply_to_vacancy(
    vacancy_id: str, resume_id: str, access_token: str, message: str = ""
):
    """
    Submits an application to a specified job vacancy on hh.ru.

    Args:
        vacancy_id (int): The ID of the vacancy to apply for.
        resume_id (str): The ID of the resume to be submitted.
        message (str): A message to accompany the application.
        access_token (str): The access token for authentication.

    Returns:
        str | None: The ID of the application if successful, or None if an error occurs.
    """
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    if message != "":
        data = {
            "resume_id": resume_id,
            "vacancy_id": vacancy_id,
            "message": message,
        }
    else:
        data = {
            "resume_id": resume_id,
            "vacancy_id": vacancy_id,
        }

    res = requests.post(
        f"https://api.hh.ru/negotiations", data=data, headers=headers
    )

    if res.status_code == 201:
        location_header = res.headers.get("Location")
        if location_header:
            nid = location_header.split("/")[-1]
            log.info(f"Успешная подача на вакансию, ID отклика: {nid}")
            return nid
        else:
            log.error("Заголовок Location отсутствует.")
            return None
    elif res.status_code == 303:
        loc = "Location"
        log.error(f"Вакансия с подачей не на hh.ru: {res.headers.get(loc)}")
        return None
    else:
        if res.json()["errors"][0]["value"] == "test_required":
            log.error("Нужно пройти тестовое задание")
            return "Нужно пройти тестовое задание"
        log.error(f"Ошибка при подаче на вакансию: {res.json()}")
        return None
