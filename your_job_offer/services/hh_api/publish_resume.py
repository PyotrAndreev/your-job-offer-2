import requests
import your_job_offer.logger as logger

log = logger.get_logger(__name__)


def publish_resume(resume_id: str, access_token: str):
    try:
        headers = {
            "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
            "Authorization": f"Bearer {access_token}",
        }

        res = requests.post(
            f"https://api.hh.ru/resumes/{resume_id}/publish", headers=headers
        )
        if res.status_code != 204:
            log.error(f"Error publishing resumes: {res.json()}")
            res = requests.get(
                f"https://api.hh.ru/resumes/{resume_id}/", headers=headers
            )
            progress = "progress"
            mandatory = "mandatory"
            log.error(f"Needed: {res.json()[progress][mandatory]}")
            return False
        else:
            log.info(f"Publish resume: {resume_id}")
            return True
    except (Timeout, ConnectionError):
        log.error("Can't connect to hh.ru while publishing resume")
        return "Can't connect to hh.ru", 503
