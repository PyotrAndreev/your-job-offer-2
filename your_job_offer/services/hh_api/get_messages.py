import requests
import logger

log = logger.get_logger(__name__)


def get_messages(nid: str, access_token: str) -> list[str]:
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }
    params = {
        "with_text_only": False,
        "locale": "RU",
        "host": "hh.ru"
    }

    res = requests.get(f"https://api.hh.ru/negotiations/{nid}/messages", headers=headers, params=params)
    responce = res.json()

    if res.status_code != 200:
        log.error(f"Error getting messages: {res.json()}")
        # raise ValueError("Error getting messages")
    else:
        return [item.get("text") for item in responce.get("items")]
