import requests
import logger

log = logger.get_logger(__name__)


def send_message(nid, mes, access_token: str):
    """
    Sends a message to a specified negotiation thread on hh.ru.

    Args:
        nid (str): The ID of the negotiation thread.
        mes (str): The message content to send.
        access_token (str): The access token for authentication.

    """
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "locale": "RU",
        "host": "hh.ru"
    }

    data = {
        "message": mes
    }

    res = requests.post(f"https://api.hh.ru/negotiations/{nid}/messages", headers=headers, params=params, data=data)

    if res.status_code != 200:
        log.error(f"Error sending message: {res.json()}")
        # raise ValueError("Bad sending message")
