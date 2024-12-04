import logger
from services.api_server.api import app

log = logger.get_logger(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    log.info("App started")
