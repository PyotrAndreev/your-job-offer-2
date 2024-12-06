import requests
import logger

log = logger.get_logger(__name__)


def get_resumes_ids(access_token: str):
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    res = requests.get("https://api.hh.ru/resumes/mine", headers=headers)
    if res.status_code != 200:
        log.error(f"Error getting resumes' ids: {res.json()}")
    else:
        data = res.json()
        log.info("Got resumes ids")
        return [item.get("id") for item in data.get("items")]
