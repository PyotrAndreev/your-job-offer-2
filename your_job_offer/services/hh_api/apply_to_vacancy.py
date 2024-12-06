import requests

import logger

log = logger.get_logger(__name__)


def apply_to_vacancy(vacancy_id: int, resume_id: str, message: str, access_token: str):
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
        "Content-Type": "application/json",
    }

    data = {
        "resume_id": resume_id,
        "vacancy_id": vacancy_id,
        "message": message,
    }

    res = requests.post(f"https://api.hh.ru/negotiations", data=data, headers=headers)

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
    else:
        log.error(f"Ошибка при подаче на вакансию: {res.json()}")
        return None
