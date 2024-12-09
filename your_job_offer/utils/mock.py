from os import getenv

from your_job_offer.entities.user import *


def get_user() -> UserModel:
    # return UserModel(
    #     login="",
    #     password="",
    #     birth_date="",
    #     first_name="Руслан",
    #     last_name="Яфаров",
    #     middle_name="",
    #     gender="",
    #     phone="+79271269651",
    #     email="afarovruslan@gmail.com",
    #     city="Долгопрудный",
    #     country="Россия",
    #     cv="https://github.com/afarovruslan",
    #     description="",
    #     work_type="",
    #     min_salary=0,
    #     max_salary=0,
    #     business_trip_readiness=0,
    #     work_hours=0,
    #     relocation=0,
    #     achievements=[
    #         AchievementModel(
    #             name="Призер регионального этапа ВСОШ",
    #             description="Призер регионального этапа ВСОШ по информатике и математике в 2022 году.",
    #             link="",
    #         ),
    #         AchievementModel(
    #             name="Хороший средний балл в ВУЗе",
    #             description="Средний балл 8.6 за последние 2 семестра, вследствие этого получаю повышенную стипендию на Физтехе.",
    #             link="",
    #         ),
    #     ],
    #     projects=[
    #         ProjectModel(
    #             name="Генерация батчей",
    #             description="Проект в рамках практики в ВШПИ, предложенный Яндексом. Идея в том, чтобы объединять несколько заказов в батч чтобы курьер меньше перемещался и больше доставлял.",
    #             link="https://github.com/shiriaevpg/batches_generation",
    #         ),
    #         ProjectModel(
    #             name="Домашка на курсе с++",
    #             description="Домашка на курсе по c++. Были реализованы своя длинная арифметика(biginteger), аналоги std::deque, std::list и другие.",
    #             link="https://github.com/afarovruslan/cplusplus_course_homework/tree/main",
    #         ),
    #         ProjectModel(
    #             name="Анализатор текста",
    #             description="Целью было по предложению определить, является оно положительным, отрицательным или нейтральным. Использовали линейные и сверточные модели машинного обучения.",
    #             link="https://github.com/orgs/hsse-mipt/repositories",
    #         ),
    #     ],
    #     # TODO skills переписать на SkillModel
    #     skills=[
    #         "Хорошее знание C++",
    #         "Опыт написания многопоточных программ",
    #         "Знание алгоритмов и структур данных",
    #         "Python",
    #         "SQL",
    #         "Docker",
    #         "git",
    #         "bash",
    #         "Понимание ассемблера",
    #     ],
    #     work_experiences=[
    #         WorkExperienceModel(
    #             id=0,
    #             job_id="Стажер",
    #             work_place="МТС",
    #             description="Дали задачу извлечь эмбеддинги из текста и сделать пайплайн.",
    #         )
    #     ],
    #     inner_email=getenv("EMAIL"),
    #     inner_email_password=getenv("EMAIL_PASSWORD"),
    # )
    return UserModel(
        login=None,
        password=None,
        id=None,
        birth_date=None,
        first_name=Name(name="Руслан"),
        last_name=Name(name="Яфаров"),
        middle_name=Name(name=""),
        photo=None,
        gender="",
        phone="+79271269651",
        email="afarovruslan@gmail.com",
        city="Долгопрудный",
        country="Россия",
        cv="https://github.com/afarovruslan",
        description="",
        work_type="",
        min_salary=None,
        max_salary=None,
        business_trip_readiness=0,
        work_hours=None,
        relocation=0,
        employment=None,
        schedule=None,
        hh_resume_id=None,
        education_level=EducationLevelEnum.UNFINISHED_HIGHER,
        source=None,
        projects=[
            ProjectModel(
                id=None,
                name="Генерация батчей",
                description="Проект в рамках практики в ВШПИ, предложенный Яндексом.",
                link="https://github.com/shiriaevpg/batches_generation",
            ),
            ProjectModel(
                id=None,
                name="Домашка на курсе с++",
                description="Домашка на курсе по c++ с реализацией длинной арифметики и других структур.",
                link="https://github.com/afarovruslan/cplusplus_course_homework/tree/main",
            ),
            ProjectModel(
                id=None,
                name="Анализатор текста",
                description="Проект в ВШПИ по определению эмоциональной окраски предложений с использованием моделей машинного обучения.",
                link="https://github.com/orgs/hsse-mipt/repositories",
            ),
        ],
        achievements=[
            AchievementModel(
                id=None,
                name="Призер регионального этапа ВСОШ",
                description="Призер по информатике и математике в 2022 году.",
                link="",
            ),
            AchievementModel(
                id=None,
                name="Абрамовка",
                description="Повышенная стипендия на Физтехе благодаря хорошему среднему баллу.",
                link="",
            ),
        ],
        work_experiences=[
            WorkExperienceModel(
                id=None,
                job="Стажер",
                work_place="МТС",
                description="Задача извлечения эмбеддингов из текста и создание пайплайна.",
                start_date="2024-03-15",
                finish_date="2024-09-13",
            )
        ],
        educations=[],
        skills=[
            "Хорошее знание c++",
            "Опыт написания многопоточных программ",
            "Знание алгоритмов и структур данных",
            "Python",
            "SQL",
            "Docker",
            "git",
            "bash",
            "Понимание Ассемблера",
        ],
        languages=[],
        vacancy=[],
        inner_email=getenv("EMAIL"),
        inner_email_password=getenv("EMAIL_PASSWORD"),
    )
