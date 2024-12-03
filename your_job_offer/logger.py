import logging

from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


def get_file_handler(name):
    file_handler = logging.FileHandler(f"app_logs/{name}.txt", mode='a')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(name))
    logger.addHandler(get_stream_handler())
    return logger


def init_sentry():
    sentry_sdk.init(
        dsn="https://c4ae42687e4ad55f3107e293cea8db25@o4508405530558464.ingest.de.sentry.io/4508405614837840",
        integrations=[FlaskIntegration(), LoggingIntegration(
            level=logging.INFO,
            event_level=logging.INFO
        ), ],
        traces_sample_rate=1.0
    )
