import logging
from logging.config import dictConfig

from .logger_settings import logger_config

dictConfig(logger_config)
logger = logging.getLogger(__name__)
