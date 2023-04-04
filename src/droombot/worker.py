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


import asyncio
import json
import logging

import aiohttp
import pydantic
import pydantic.json
import redis.asyncio as redis
from aiolimiter import AsyncLimiter

from .api import text_to_image
from .config import MAX_REQUESTS_PER_MINUTE, REDIS_HOST, REDIS_KEY_LIFETIME, REDIS_PORT
from .models import PubSubMessage, TextPrompt, TextToImageRequest

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self):
        self._redis_connection = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def run(self):
        logger.info("Starting worker...")
        asyncio.run(self.loop())

    async def loop(self):
        """Main application loop"""
        http_client = aiohttp.ClientSession()
        limiter = AsyncLimiter(MAX_REQUESTS_PER_MINUTE)
        async with self._redis_connection.pubsub() as pubsub:
            await pubsub.subscribe("droombot-prompts")
            while True:
                async with limiter:
                    asyncio.ensure_future(self.read_and_run(pubsub, http_client))

    async def read_and_run(
        self, channel: redis.client.PubSub, session: aiohttp.ClientSession
    ) -> None:
        """Read redis channel for new message, and run text-to-image if there is one.

        The result is stored back into redis by the interaction id

        :return: None
        """
        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is None:
            logger.debug("No message to process...")
            return

        try:
            deserialized_message = PubSubMessage.parse_raw(message["data"])
        except pydantic.ValidationError as e:
            logger.error(f"Could not parse message from pubsub due to: {e}")
            return

        logger.info(
            "Received message with for interaction "
            f"{deserialized_message.interaction_id} with prompt: "
            f"'{deserialized_message.text_prompt}'"
        )

        text_to_image_request = TextToImageRequest(
            text_prompts=[TextPrompt(text=deserialized_message.text_prompt, weight=1.0)]
        )

        logger.info("Running text-to-image conversion")
        responses = await text_to_image(session, text_to_image_request)
        logger.info("Received response from text-to-image conversion")
        serialized_responses = json.dumps(
            responses, default=pydantic.json.pydantic_encoder
        )

        logger.info("Storing result in redis.")
        await self._redis_connection.set(
            f"interaction:{deserialized_message.interaction_id}",
            serialized_responses,
            ex=REDIS_KEY_LIFETIME,
        )
        logger.info("Stored result in redis.")
