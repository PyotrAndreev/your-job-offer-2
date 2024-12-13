from your_job_offer.repository.vacancies_repository.utils import professional_roles
from your_job_offer.repository.vacancies_repository.db_methods import save_role

def get_professional_roles():
    for role in professional_roles:
        save_role(ProfessionalRole(roleId=role["id"], name=role["role"]))
        