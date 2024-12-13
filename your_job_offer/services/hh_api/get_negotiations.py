import requests
import your_job_offer.logger as logger

log = logger.get_logger(__name__)


def get_negotiations(access_token: str):
    """
    Retrieves a list of negotiation threads from hh.ru.

    Args:
        access_token (str): The access token for authentication.

    Returns:
        list[str]: A list of negotiation thread IDs.
    """
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    res = requests.get("https://api.hh.ru/negotiations", headers=headers)
    responce = res.json()
    if res.status_code != 200:
        log.error(f"Error getting negotiations: {res.json()}")
    else:
        log.info("Got negotiations")
        return [item.get("id") for item in responce.get("items")]
