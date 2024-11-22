from os import getenv

from your_job_offer.domain.models.user import *


def get_user() -> User:
    return User(
        birth_date="",
        first_name=Name(name="Руслан"),
        last_name=Name(name="Яфаров"),
        middle_name=Name(name=""),
        gender="",
        phone=Phone(phohe="+79271269651"),
        email=Email(email="afarovruslan@gmail.com"),
        city="Долгопрудный",
        country="Россия",
        cv="https://github.com/afarovruslan",
        description="",
        work_type="",
        min_salary=Salary(salary=""),
        max_salary=Salary(salary=""),
        business_trip_readiness=0,
        work_hours=WorkHours(hours=""),
        relocation=0,
        achievements=[
            Achievement(
                title="Призер регионального этапа ВСОШ",
                description="Призер регионального этапа ВСОШ по информатике и математике в 2022 году.",
                link="",
            ),
            Achievement(
                title="Хороший средний балл в ВУЗе",
                description="Средний балл 8.6 за последние 2 семестра, вследствие этого получаю повышенную стипендию на Физтехе.",
                link="",
            ),
        ],
        projects=[
            Project(
                title="Генерация батчей",
                description="Проект в рамках практики в ВШПИ, предложенный Яндексом. Идея в том, чтобы объединять несколько заказов в батч чтобы курьер меньше перемещался и больше доставлял.",
                link="https://github.com/shiriaevpg/batches_generation",
            ),
            Project(
                title="Домашка на курсе с++",
                description="Домашка на курсе по c++. Были реализованы своя длинная арифметика(biginteger), аналоги std::deque, std::list и другие.",
                link="https://github.com/afarovruslan/cplusplus_course_homework/tree/main",
            ),
            Project(
                title="Анализатор текста",
                description="Целью было по предложению определить, является оно положительным, отрицательным или нейтральным. Использовали линейные и сверточные модели машинного обучения.",
                link="https://github.com/orgs/hsse-mipt/repositories",
            ),
        ],
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
        work_experience=[
            WorkExperience(
                job="Стажер",
                work_place="МТС",
                description="Дали задачу извлечь эмбеддинги из текста и сделать пайплайн.",
                start_date="2024-03-15",
                finish_date="2024-09-13",
            )
        ],
        inner_email=getenv("EMAIL"),
        inner_email_password=getenv("EMAIL_PASSWORD"),
    )
