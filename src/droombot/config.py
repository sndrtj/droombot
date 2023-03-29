import os

STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")

# Token for discord bot
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# Discord guilds ids to use for the bot. Set these when testing and
# developing. Registering a global slash command takes a long time (1hr+), so use
# a guild id when testing. If not set or empty string, we will register a global
# slash command.
DISCORD_GUILD_IDS = [
    item for item in os.environ.get("DISCORD_GUILD_IDS", "").split(",") if item != ""
]
