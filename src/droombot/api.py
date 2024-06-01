#    Copyright 2023-2024 Sander Bollen
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
import logging

import aiohttp

from .config import STABILITY_API_KEY
from .models import (
    TextToImageRequestV2Core,
    TextToImageRequestV2SD3,
    TextToImageResponse,
)
from .version import VERSION

logger = logging.getLogger(__name__)

CORE_TEXT_TO_IMAGE_BASE_URL = (
    "https://api.stability.ai/v2beta/stable-image/generate/core"
)
SD3_TEXT_TO_IMAGE_BASE_URL = "https://api.stability.ai/v2beta/stable-image/generate/sd3"


async def text_to_image(
    session: aiohttp.ClientSession,
    request: TextToImageRequestV2Core | TextToImageRequestV2SD3,
    timeout: int = 300,
) -> list[TextToImageResponse]:
    """Call Stability with a text to image request

    :param session: AIOhttp session
    :param request: the incoming request
    :param timeout: timeout in seconds, defaults to 300. Don't set too low, as
        image generation takes some time.
    :return: list of responses, one for each text prompt
    :raises: timeout
    """
    match request:
        case TextToImageRequestV2Core():
            logger.info("Incoming call for text-to-image generation for Core")
            url = CORE_TEXT_TO_IMAGE_BASE_URL
        case TextToImageRequestV2SD3():
            logger.info("Incoming call for text-to-image generation for SD3")
            url = SD3_TEXT_TO_IMAGE_BASE_URL
        case _:
            raise ValueError(f"Unsupported request: {type(request)}")

    user_agent = f"droombot/{VERSION}"
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "User-Agent": user_agent,
        "accept": "application/json",
    }

    raw_post_data = request.model_dump(mode="json")
    writer = aiohttp.MultipartWriter("form-data")
    # filter out values that are None
    for k, v in raw_post_data.items():
        if v is None:
            continue
        writer.append(
            aiohttp.StringPayload(value=str(v)),
            headers={aiohttp.hdrs.CONTENT_DISPOSITION: f'form-data; name="{k}"'},
        )

    async with session.post(
        url=url, data=writer, timeout=timeout, headers=headers
    ) as resp:
        results = await resp.json()
        if resp.status >= 400:
            logger.error(f"Call to Stability errored. Response: {results}")
            raise ValueError("An error occurred")

    # responses are encoded in an 'artifacts' item, but this is NOT
    # mentioned in the docs.
    logger.info("Received a successful response from text-to-image generation.")
    return [TextToImageResponse.from_raw_api(results)]


if __name__ == "__main__":
    # for testing
    async def main():
        request = TextToImageRequestV2Core(
            prompt="Green trees in a forest with ferns, oil painting"
        )
        async with aiohttp.ClientSession() as session:
            results = await text_to_image(session, request)

        print(results[0].model_dump_json())

    asyncio.run(main())
