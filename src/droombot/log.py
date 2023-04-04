#    Copyright 2023 Sander Bollen
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


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
