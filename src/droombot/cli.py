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
