import logging

import click

from .log import init_logging

logger = logging.getLogger(__name__)


init_logging()


@click.command("droombot")
def droombot():
    logger.info("Starting application...")
