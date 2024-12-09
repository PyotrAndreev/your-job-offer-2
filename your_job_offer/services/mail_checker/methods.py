from .inner import get_messages
from your_job_offer.entities.user import UserModel, EmailMessage


def get_email_messages(user: UserModel) -> list[EmailMessage]:
    return get_messages(user.inner_email, user.inner_email_password)
