import logging
import logging.config

logger = logging.getLogger(__name__)


def init_logging():
    """Initialize logging

    Set up logging handler to stdout, with friendly format.

    Should be called at application bootup.

    :return: None
    """
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": (
                        "[%(asctime)s] - %(levelname)s - %(message)s - "
                        "[%(filename)s:%(lineno)d]"
                    )
                }
            },
            "handlers": {
                "default": {
                    "level": "DEBUG",
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "droombot": {"handlers": ["default"], "level": "DEBUG"},
            },
        }
    )
