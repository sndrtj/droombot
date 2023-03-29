import logging

import aiohttp
import discord

from .api import text_to_image
from .config import DISCORD_GUILD_IDS
from .models import FinishReason, TextToImageRequest
from .utils import text_to_image_result_to_buffer

logger = logging.getLogger(__name__)

bot = discord.Bot()


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
            f"Hi {ctx.interaction.user.name}. Your prompt text may not be empty"
        )
        return

    await ctx.respond(
        f"Hi {ctx.interaction.user.name}! We will now be generating your image. "
        f"This may take a minute."
    )
    request = TextToImageRequest(text_prompts=[{"text": text, "weight": 1.0}])

    logger.info("Firing off request to Stability")
    # FIXME session and error handling
    # Could also use some abstraction
    image_results = await text_to_image(aiohttp.ClientSession(), request)
    if not all(r.finish_reason is FinishReason.SUCCESS for r in image_results):
        # FIXME: say why.
        await ctx.respond("Image generation failed - please try again later.")
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
