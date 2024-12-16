import your_job_offer.logger as logger
from your_job_offer.services.api_server.api import app

log = logger.get_logger(__name__)
emails = [], passwords = []


def extract_emails_and_passwords(file_path: str):
    emails = []
    passwords = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if ':' in line:
                email, password = line.split(':', 1)
                emails.append(email)
                passwords.append(password)

    return emails, passwords


if __name__ == "__main__":
    log.info("App started")
    emails, passwords = extract_emails_and_passwords("../secrets/mail.txt")
    app.run(host="0.0.0.0", port=8080)
