import logger
from entities.hh_token import HHTokenModel
import requests

from services.tokens_repository.db_methods import update_hh_token

log = logger.get_logger(__name__)


def refresh_hh_token(hh_token: HHTokenModel):
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
    }

    params = {
        "grant_type": "refresh_token",
        "refresh_token": hh_token.refresh_token
    }

    res = requests.post("https://hh.ru/oauth/token", headers=headers, params=params)
    responce = res.json()
    if res.status_code != 200:
        log.error(f"Error refreshing hh token: {res.json()}")
        # raise ValueError("Error refreshing hh token")
    else:
        hh_token.access_token = responce.get("access_token")
        hh_token.refresh_token = responce.get("refresh_token")
        update_hh_token(hh_token)
