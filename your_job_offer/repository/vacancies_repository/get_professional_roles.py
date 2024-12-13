from your_job_offer.repository.vacancies_repository.utils import professional_roles
from your_job_offer.repository.vacancies_repository.db_methods import save_role
import your_job_offer.logger as logger

log = logger.get_logger(__name__)

def get_professional_roles():
    for role in professional_roles:
        professional_role = ProfessionalRole(roleId=role["id"], name=role["role"])
        log.info(f"Saved {professional_role}")
        save_role(professional_role)
