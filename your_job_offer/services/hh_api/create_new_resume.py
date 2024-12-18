import requests
import your_job_offer.logger as logger
from your_job_offer.entities.user import UserModel
from your_job_offer.services.hh_api.utils import (
    employment_id_name,
    relocation_id_name,
    schedule_id_name,
    languages,
    language_level_id_name,
    education_level_id_name,
)

log = logger.get_logger(__name__)


def create_new_resume(user: UserModel, access_token: str):
    try:
        headers = {
            "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
            "Authorization": f"Bearer {access_token}",
        }

        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name if user.middle_name != '' else None,
            "birth_date": user.birth_date[:10] if user.birth_date != '' and user.birth_date else None,
            "gender": {
                "id": user.gender.value if user.gender else None,
            },
            "area": {
                "id": user.city.area_id,
            } if user.city else None,
            "citizenship": [
                {
                    "id": user.country.area_id if user.country and user.country.area_id else 113,
                },
            ],
            "contact": [
                {
                    "type": {
                        "id": "email",
                        "name": "Эл. почта",
                    },
                    "value": user.inner_email if user.inner_email else user.email,
                    "preferred": True,
                },
                {
                    "type": {
                        "id": "cell",
                        "name": "Мобильный телефон",
                    },
                    "value": {
                        "formatted": 79806253660,
                    },
                },
            ],
            "skill_set": [f"{skill.name}: {skill.description}" for skill in user.skills]
            if user.skills
            else None,
            "experience": [
                {
                    "company": exp.work_place,
                    "position": exp.job,
                    "description": exp.description,
                    "start": (
                        exp.start_date[:10] if exp.start_date else None
                    ),
                    "end": (
                        exp.finish_date[:10] if exp.finish_date else None
                    ),
                }
                for exp in user.work_experiences
            ],
            "education": {
                "level": {
                    "id": user.education_level.value,
                    "name": education_level_id_name.get(user.education_level.value),
                },
                "primary": [
                    {
                        "name": edu.institution if edu.institution else "MIPT",
                        "year": edu.finish_date[:4] if edu.finish_date else "2026",
                    }
                    for edu in user.educations
                ],
            },
            "language": [
                {
                    "id": languages.get(lang.name),
                    "name": lang.name,
                    "level": {
                        "id": lang.level.value,
                        "name": language_level_id_name.get(lang.level.value),
                    },
                }
                for lang in user.languages
            ],
            "salary":
                {
                    "amount": user.min_salary,
                    "currency": "RUR",
                }
                if user.min_salary
                else None,
            "relocation":
                {
                    "type":
                        {
                            "id": user.relocation.value,
                            "name": relocation_id_name.get(user.relocation.value),
                        },
                }
                if user.relocation else None,
            "business_trip_readiness": {
                "id": user.business_trip_readiness.value
            }
            if user.business_trip_readiness else None,
            "employments": [
                {
                    "id": user.employment.value,
                    "name": employment_id_name.get(user.employment.value),
                },
            ]
            if user.employment else None,
            "schedules":
                [
                    {
                        "id": user.schedule.value,
                        "name": schedule_id_name.get(user.schedule.value)
                    },
                ]
                if user.schedule else None,
            "professional_roles": [
                {
                    "id": user.professional_role.role_id,
                } if user.professional_role else {"id": 156},
            ],
            "title": user.professional_role.name if user.professional_role else None,
        }

        data = {k: v for k, v in data.items() if v is not None}
        log.info(f"Data for resume: {data}")

        res = requests.post("https://api.hh.ru/resumes", headers=headers, json=data)

        if res.status_code == 201:
            log.info(f"Resume added")
            location_header = res.headers.get("Location")
            if location_header:
                resume_id = location_header.split("/")[-1]
                log.info(f"Successful create resume ID: {resume_id}")
                return resume_id, 200
            else:
                log.error("Header Location isn't present")
                return "Header Location isn't present", 404
        elif res.status_code == 400:
            log.error(f"Error in the request parameters: {res.json()}")
            return "Error in the request parameters", 400
        elif res.status_code == 403:
            log.error(f"Error in authorization: {res.json()}")
            return "Error in authorization", 403
        else:
            log.error(f"Error while creating resume: {res.json()}")
            return f"Error while creating resume: {res.json()}", 520
    except (Timeout, ConnectionError):
        log.error("Can't connect to hh.ru while creating new resume")
        return "Can't connect to hh.ru", 503
