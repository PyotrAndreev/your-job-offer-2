import your_job_offer.logger as logger
from your_job_offer.entities.hh_token import HHTokenModel
import requests

from your_job_offer.repository.tokens_repository.db_methods import (
    update_hh_token,
)

log = logger.get_logger(__name__)


def refresh_hh_token(hh_token: HHTokenModel):
    try:
        headers = {
            "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        }

        params = {
            "grant_type": "refresh_token",
            "refresh_token": hh_token.refresh_token,
        }

        res = requests.post(
            "https://hh.ru/oauth/token", headers=headers, params=params
        )
        responce = res.json()
        if res.status_code != 200:
            log.warning(f"Refreshing hh token failed: {res.json()}")
            return "Refreshing hh token failed", 404
        else:
            log.info(f"Refreshed hh token: {res.json()}")
            hh_token.access_token = responce.get("access_token")
            hh_token.refresh_token = responce.get("refresh_token")
            update_hh_token(hh_token)
            return "", 200
    except (TimeoutError, ConnectionError):
        log.error("Can't connect to hh.ru while refreshing hh token")
        return "Can't connect to hh.ru", 503
