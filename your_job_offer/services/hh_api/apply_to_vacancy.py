import requests

import your_job_offer.logger as logger

log = logger.get_logger(__name__)


def apply_to_vacancy(
    vacancy_id: str, resume_id: str, access_token: str, message: str = ""
):
    try:
        headers = {
            "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
            "Authorization": f"Bearer {access_token}",
        }

        if message != "":
            data = {
                "resume_id": resume_id,
                "vacancy_id": vacancy_id,
                "message": message,
            }
        else:
            data = {
                "resume_id": resume_id,
                "vacancy_id": vacancy_id,
            }

        res = requests.post(
            f"https://api.hh.ru/negotiations", data=data, headers=headers
        )

        if res.status_code == 201:
            location_header = res.headers.get("Location")
            if location_header:
                nid = location_header.split("/")[-1]
                log.info(f"Succesful applying, ID: {nid}")
                return nid, 200
            else:
                log.error("Header Location isn't present")
                return "Header Location isn't present", 404
        elif res.status_code == 303:
            loc = "Location"
            log.warning(f"Vacancy with applying not on hh.ru: {res.headers.get(loc)}")
            return "Vacancy with applying not on hh.ru: {res.headers.get(loc)}", 303
        elif res.status_code == 400:
            log.error(f"Error in the request parameters: {res.json()}")
            return "Error in the request parameters", 400
        else:
            if res.json()["errors"][0]["value"] == "test_required":
                log.warning("Test required")
                return "Test required", 302
            log.error(f"Error during applying: {res.json()}")
            return f"Error during applying: {res.json()}", 520
    except (Timeout, ConnectionError):
        log.error("Can't connect to hh.ru while applying")
        return "Can't connect to hh.ru", 503
