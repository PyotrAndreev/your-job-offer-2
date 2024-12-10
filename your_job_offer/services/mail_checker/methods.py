from .inner import get_messages
from your_job_offer.entities.user import UserModel, EmailMessage


def get_email_messages(user: UserModel) -> list[EmailMessage]:
    return get_messages(user.inner_email, user.inner_email_password)


def get_new_email(
    filename="your_job_offer/services/mail_checker/mails.txt",
) -> tuple[str, str]:
    """
    Return new email and password from file
    """
    with open(filename, "r") as file:
        lines = file.readlines()

    first_line = lines[0]
    lines = lines[1:]

    with open(filename, "w") as file:
        file.writelines(lines)
    login, password = first_line.split(":")
    return login, password[:-1]
