from os import getenv

from entities.user import UserModel, AchievementModel, ProjectModel, WorkExperienceModel


def get_user() -> UserModel:
    return UserModel(
        birth_date="",
        first_name="Руслан",
        last_name="Яфаров",
        middle_name="",
        gender="",
        phone="+79271269651",
        email="afarovruslan@gmail.com",
        city="Долгопрудный",
        country="Россия",
        cv="https://github.com/afarovruslan",
        description="",
        work_type="",
        min_salary=0,
        max_salary=0,
        business_trip_readiness=0,
        work_hours=0,
        relocation=0,
        achievements=[
            AchievementModel(

                name="Призер регионального этапа ВСОШ",
                description="Призер регионального этапа ВСОШ по информатике и математике в 2022 году.",
                link="",
            ),
            AchievementModel(
                name="Хороший средний балл в ВУЗе",
                description="Средний балл 8.6 за последние 2 семестра, вследствие этого получаю повышенную стипендию на Физтехе.",
                link="",
            ),
        ],
        projects=[
            ProjectModel(
                name="Генерация батчей",
                description="Проект в рамках практики в ВШПИ, предложенный Яндексом. Идея в том, чтобы объединять несколько заказов в батч чтобы курьер меньше перемещался и больше доставлял.",
                link="https://github.com/shiriaevpg/batches_generation",
            ),
            ProjectModel(
                name="Домашка на курсе с++",
                description="Домашка на курсе по c++. Были реализованы своя длинная арифметика(biginteger), аналоги std::deque, std::list и другие.",
                link="https://github.com/afarovruslan/cplusplus_course_homework/tree/main",
            ),
            ProjectModel(
                name="Анализатор текста",
                description="Целью было по предложению определить, является оно положительным, отрицательным или нейтральным. Использовали линейные и сверточные модели машинного обучения.",
                link="https://github.com/orgs/hsse-mipt/repositories",
            ),
        ],
        # TODO skills переписать на SkillModel
        skills=[

            "Хорошее знание C++",
            "Опыт написания многопоточных программ",
            "Знание алгоритмов и структур данных",
            "Python",
            "SQL",
            "Docker",
            "git",
            "bash",
            "Понимание ассемблера",
        ],
        work_experiences=[
            WorkExperienceModel(
                id=0,
                job_id="Стажер",
                work_place="МТС",
                description="Дали задачу извлечь эмбеддинги из текста и сделать пайплайн.",

            )
        ],
        inner_email=getenv("EMAIL"),
        inner_email_password=getenv("EMAIL_PASSWORD"),
    )
