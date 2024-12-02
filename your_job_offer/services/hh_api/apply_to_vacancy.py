import requests

import logger

log = logger.get_logger(__name__)


def apply_to_vacancy(vacancy_id: int, resume_id: str, message: str, access_token: str):
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
        log.error(f"Вакансия с подачей не на hh.ru: {res.headers.get("Location")} ")
    else:
        log.error(f"Ошибка при подаче на вакансию: {res.json()}")
        return None
