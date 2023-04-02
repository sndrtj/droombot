import logging
import time

import aiolimiter
import discord
import pydantic
import redis.asyncio as redis

from .config import DISCORD_GUILD_IDS, MAX_REQUESTS_PER_MINUTE, REDIS_HOST, REDIS_PORT
from .models import FinishReason, PubSubMessage, TextToImageResponse
from .utils import text_to_image_result_to_buffer

logger = logging.getLogger(__name__)


LIMITER = aiolimiter.AsyncLimiter(MAX_REQUESTS_PER_MINUTE)


async def poll_interaction_result(
    redis_connection: redis.Redis, interaction_id: str, timeout: int = 900
) -> list[TextToImageResponse]:
    """Poll the interaction result from redis

    :param redis_connection: Redis instance to poll from
    :param interaction_id: interaction id to retrieve
    :param timeout: timeout in seconds, after which we bail
    :return: list of text to image repsonses
    :raises: TimeOutError
    """
    interaction_key = f"interaction:{interaction_id}"
    start = time.monotonic()
    while True:
        now = time.monotonic()
        if (now - start) >= timeout:
            raise TimeoutError("Waited for too long, no result found")
        async with LIMITER:
            logger.debug(f"Polling for {interaction_key}")
            raw_results = await redis_connection.get(interaction_key)
        if raw_results is None:
            logger.debug(f"Interaction {interaction_key} not found, trying again")
            continue

        logger.debug("Found results, parsing to response")
        return pydantic.parse_raw_as(list[TextToImageResponse], raw_results)


def create_bot() -> discord.Bot:
    """Create the discord bot

    :return:
    """
    bot = discord.Bot()
    redis_connection: redis.Redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    @bot.event
    async def on_ready():
        logger.info(f"Starting bot as {bot.user}...")

    @bot.slash_command(
        description="Generate images using a text prompt", guild_ids=DISCORD_GUILD_IDS
    )
    async def prompt(ctx, text: str):
        logger.info(
            f"Receiving prompt from channel {ctx.interaction.channel_id}, "
            f"from user {ctx.interaction.user.id}"
        )
        logger.info(f"Prompt message: {text}")
        if text == "":
            await ctx.respond(
                f"Hi {ctx.interaction.user.mention}. Your prompt text may not be empty"
            )
            return

        await ctx.respond(
            f"Hi {ctx.interaction.user.mention}! Your prompt: **{text}**. "
            "We will now be generating your image. "
            "This may take a minute."
        )

        logger.info("Sending message to redis for worker to pick up")
        message = PubSubMessage(
            interaction_id=str(ctx.interaction.id), text_prompt=text
        )

        await redis_connection.publish("droombot-prompts", message.json())
        logger.info("Polling for result")

        try:
            image_results = await poll_interaction_result(
                redis_connection, str(ctx.interaction.id)
            )
        except TimeoutError:
            logger.error("Received timeout on polling for results...")
            await ctx.respond("Image generation failed - please try again later.")
            return
        logger.info("Results received, converting to files")

        if not all(r.finish_reason is FinishReason.SUCCESS for r in image_results):
            is_error = any(r.finish_reason is FinishReason.ERROR for r in image_results)
            is_filtered = any(
                r.finish_reason is FinishReason.CONTENT_FILTERED for r in image_results
            )
            if is_error:
                await ctx.respond(
                    "Image generation failed to due to error - please try again later"
                )
            elif is_filtered:
                await ctx.respond(
                    "Image generation failed due to prompt being filtered. "
                    "Please try another prompt."
                )
            else:
                await ctx.respond("Image generation failed due to unknown error.")
            return

        logger.info("Converting response to buffers")

        files = []
        for i, image_result in enumerate(image_results):
            buffer = text_to_image_result_to_buffer(image_result)
            file = discord.File(
                buffer, filename=f"{ctx.interaction.user.name}_{text[:10]}_{i}.png"
            )
            files.append(file)
        logger.info("Done converting to buffers")

        await ctx.respond("Here are the results!", files=files)

    return bot
