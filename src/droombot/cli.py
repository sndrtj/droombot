import logging

import click

from .bot import bot
from .config import DISCORD_BOT_TOKEN
from .log import init_logging

logger = logging.getLogger(__name__)


init_logging()


@click.command("droombot")
def droombot():
    logger.info("Starting application...")
    bot.run(DISCORD_BOT_TOKEN)
