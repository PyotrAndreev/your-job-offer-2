import requests
import your_job_offer.logger as logger

log = logger.get_logger(__name__)


def delete_cv(resume_id: str, access_token: str):
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    res = requests.get(
        f"https://api.hh.ru/resumes/{resume_id}", headers=headers
    )
    if res.status_code != 204:
        log.error(f"Error deleting resumes: {res.json()}")
    else:
        log.info(f"Delete resume: {resume_id}")
