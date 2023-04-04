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


import os

STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY")

# Token for discord bot
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# Discord guilds ids to use for the bot. Comma-separated values.
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
