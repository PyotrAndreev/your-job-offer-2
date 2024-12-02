import requests
import logger

log = logger.get_logger(__name__)


def get_negotiations(access_token: str):
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    res = requests.get("https://api.hh.ru/negotiations", headers=headers)
    responce = res.json()
    if res.status_code != 200:
        log.error(f"Error getting negotiations: {res.json()}")
        # raise ValueError("Error getting negotiations")
    else:
        return [item.get("id") for item in responce.get("items")]
