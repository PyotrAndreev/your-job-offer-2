import your_job_offer.logger as logger
from your_job_offer.services.api_server.api import app

from your_job_offer.use_cases.emails import extract_emails_and_passwords

log = logger.get_logger(__name__)


if __name__ == "__main__":
    log.info("App started")
    emails, passwords = extract_emails_and_passwords("../secrets/mail.txt")
    app.run(host="0.0.0.0", port=8080)
