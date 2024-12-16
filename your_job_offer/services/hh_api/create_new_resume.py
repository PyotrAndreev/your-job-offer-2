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
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "middle_name": user.middle_name if user.middle_name != '' else None,
        "birth_date": user.birth_date,
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
        # "experience": [
        #     {
        #         "company": exp.work_place,
        #         "position": exp.job,
        #         "description": exp.description,
        #         "start": (
        #             exp.start_date.isoformat() if exp.start_date else None
        #         ),
        #         "end": (
        #             exp.finish_date.isoformat() if exp.finish_date else None
        #         ),
        #     }
        #     for exp in user.work_experiences
        # ],
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
            else None
        ,
        # "relocation":
        #     {
        #         "type":
        #             {
        #                 "id": user.relocation.value,
        #                 "name": relocation_id_name.get(user.relocation.value),
        #             },
        #     }
        #     if user.relocation else None,
        # "business_trip_readiness": {
        #     "id": user.business_trip_readiness.value
        # }
        # if user.business_trip_readiness else None,
        # "employments": [
        #     {
        #         "id": user.employment.value,
        #         "name": employment_id_name.get(user.employment.value),
        #     },
        # ]
        # if user.employment else None,
        # "schedules":
        #     [
        #         {
        #             "id": user.schedule.value,
        #             "name": schedule_id_name.get(user.schedule.value)
        #         },
        #     ]
        #     if user.schedule else None,
        "professional_roles": [
            {
                "id": user.professional_role.role_id,
            } if user.professional_role else {"id": 156},
        ],
        "title": user.professional_role.name if user.professional_role else None,
    }

    data = {k: v for k, v in data.items() if v is not None}
    print(data)

    res = requests.post("https://api.hh.ru/resumes", headers=headers, json=data)
    if res.status_code != 201:
        log.error(res.status_code)
        log.error(f"Error adding resume: {res.json()}")
        return None
    else:
        log.info(f"Resume added")
        location_header = res.headers.get("Location")
        if location_header:
            resume_id = location_header.split("/")[-1]
            log.info(f"Резюме успешно создано с ID: {resume_id}")
            return resume_id
        else:
            log.error("Не удалось получить ID резюме из заголовков ответа.")
            return None
