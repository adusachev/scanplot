import logging

logger_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "base_formatter": {
            "format": "%(levelname)s - %(filename)s - %(funcName)s: %(message)s",
            "class": "logging.Formatter",
        }
    },
    "handlers": {
        "base_handler": {
            "class": "logging.StreamHandler",
            "level": logging.DEBUG,
            "formatter": "base_formatter",
        }
    },
    "loggers": {"scanplot": {"level": logging.DEBUG, "handlers": ["base_handler"]}},
}
