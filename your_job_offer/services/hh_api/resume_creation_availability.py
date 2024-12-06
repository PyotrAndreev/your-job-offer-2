import requests
import logger

log = logger.get_logger(__name__)


def is_resume_creation_available(access_token: str) -> bool:
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    res = requests.get("https://api.hh.ru/resumes/creation_availability", headers=headers)
    if res.status_code != 200:
        log.error(f"Error checking possibility of creation resume: {res.json()}")
    else:
        data = res.json()
        field = "is_creation_available"
        log.info(f"Creation availability: {data.get(field)}")
        return data.get("is_creation_available")
