import requests
import logger
from entities.user import UserModel
from services.hh_api.utils import employment_id_name, relocation_id_name, schedule_id_name, languages, \
    language_level_id_name, education_level_id_name

log = logger.get_logger(__name__)


def create_new_resume(user: UserModel, access_token: str):
    headers = {
        "HH-User-Agent": "YourJobOffer (zaitseva.dr@phystech.edu)",
        "Authorization": f"Bearer {access_token}",
    }

    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "middle_name": user.middle_name,
        "birth_date": user.birth_date,
        "gender": {
            "id": user.gender.value if user.gender else None,
        },
        "area": user.city.area_id if user.city else None,
        "contact": [
            {
                "type": {
                    "id": "email",
                    "name": "Эл. почта",
                },
                "value": user.email,
                "preferred": True,
            },
        ],
        "skill_set": [f"{skill.name}: {skill.description}" for skill in user.skills] if user.skills else None,
        "experience": [
            {
                "company": exp.work_place,
                "position": exp.job,
                "description": exp.description,
                "start": exp.start_date.isoformat() if exp.start_date else None,
                "end": exp.finish_date.isoformat() if exp.finish_date else None,
            }
            for exp in user.work_experiences
        ],
        "education": {
            "level": {
                "id": user.education_level,
                "name": education_level_id_name.get(user.education_level)
            },
            "primary": [
                {
                    "name": edu.institution,
                    "year": edu.finish_date.year if edu.finish_date else None,
                }
                for edu in user.educations
            ],
        },
        "language": [
            {
                "id": languages.get(lang.name),
                "name": lang.name,
                "level": {
                    "id": lang.level,
                    "name": language_level_id_name.get(lang.level)
                }
            }
            for lang in user.languages
        ],
        "salary": {
            "amount": user.min_salary,
            "currency": "RUR",
        } if user.min_salary else None,
        "relocation": {
            "type": {
                "id": user.relocation.value if user.relocation else None,
                "name": relocation_id_name.get(user.relocation.value) if user.relocation else None,
            } if user.relocation else None,
        } if user.relocation else None,
        "business_trip_readiness": {
            user.business_trip_readiness.value if user.business_trip_readiness else None,
        } if user.employment else None,
        "employments": [
            {
                "id": user.employment.value if user.employment else None,
                "name": employment_id_name.get(user.employment.value) if user.employment else None
            },
        ] if user.employment else None,
        "schedules": [
            {
                "id": user.schedule.value if user.schedule else None,
                "name": schedule_id_name.get(user.schedule.value) if user.schedule else None
            },
        ] if user.schedule else None,
        "professional_roles": [156,
                               160, 10, 12, 150, 25, 165, 34, 36, 73, 155,
                               96, 164, 104, 157, 107, 112, 113, 148, 114, 116, 121, 124, 125, 126],
    }

    data = {k: v for k, v in data.items() if v is not None}

    res = requests.get("https://api.hh.ru/resumes", headers=headers, data=data)
    if res.status_code != 201:
        log.error(f"Error adding resume: {res.json()}")
    else:
        log.info(f"Resume added")
        location_header = res.headers.get("Location")
        if location_header:
            resume_id = location_header.split("/")[-1]
            log.info(f"Резюме успешно создано с ID: {resume_id}")
            return resume_id
        else:
            log.error("Не удалось получить ID резюме из заголовков ответа.")
