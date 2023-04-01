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


# Redis settings
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
# how long keys set in redis need to live before being deleted, in seconds.
REDIS_KEY_LIFETIME = int(os.environ.get("REDIS_KEY_LIFETIME", 300))

# Concurrency settings
# Maximum number of requests per minute to redis and Stability. Note that
# bursty behaviour may still happen, as long as it stays less than the maximum.
MAX_REQUESTS_PER_MINUTE = int(os.environ.get("MAX_REQUESTS_PER_MINUTE", 100))
