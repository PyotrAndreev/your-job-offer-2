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

        if res.status_code == 204:
            log.info(f"Publish resume: {resume_id}")
            return "", 200
        elif res.status_code == 400:
            log.error(f"Publication or extension is not possible: {res.json()}")
            res = requests.get(
                f"https://api.hh.ru/resumes/{resume_id}/", headers=headers
            )
            progress = "progress"
            mandatory = "mandatory"
            log.error(f"Needed: {res.json()[progress][mandatory]}")
            return "Publication or extension is not possible", 400
        elif res.status_code == 403:
            log.error(f"Error in authorization: {res.json()}")
            return "Error in authorization", 403
        elif res.status_code == 429:
            log.error("Resume publication is not available")
            return "Resume publication is not available", 429
        else:
            log.error(f"Error while publishing resume: {res.json()}")
            return f"Error while publishing resume: {res.json()}", 520
    except (TimeoutError, ConnectionError):
        log.error("Can't connect to hh.ru while publishing resume")
        return "Can't connect to hh.ru", 503
