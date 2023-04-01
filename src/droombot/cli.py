import logging

import click

from .bot import create_bot
from .config import DISCORD_BOT_TOKEN
from .log import init_logging
from .worker import Worker

logger = logging.getLogger(__name__)


init_logging()


@click.group()
def cli():
    pass


@cli.command("server")
def server():
    logger.info("Starting server application...")
    bot = create_bot()
    bot.run(DISCORD_BOT_TOKEN)


@cli.command("worker")
def worker():
    logger.info("Starting worker application...")
    w = Worker()
    w.run()
