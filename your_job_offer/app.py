import your_job_offer.logger as logger
from your_job_offer.services.api_server.api import app


log = logger.get_logger(__name__)


if __name__ == "__main__":
    log.info("App started")
    app.run(host="0.0.0.0", port=8080)
