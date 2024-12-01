import logging

from .logger_settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger(__name__)
