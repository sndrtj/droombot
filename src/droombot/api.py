import asyncio
import json
import logging

import aiohttp

from .config import STABILITY_API_KEY
from .models import TextToImageRequest, TextToImageResponse
from .version import VERSION

logger = logging.getLogger(__name__)

TEX_TO_IMAGE_BASE_URL = "https://api.stability.ai/v1/generation"


async def text_to_image(
    session: aiohttp.ClientSession, request: TextToImageRequest, timeout: int = 300
) -> list[TextToImageResponse]:
    """Call Stability with a text to image request

    :param session: AIOhttp session
    :param request: the incoming request
    :param timeout: timeout in seconds, defaults to 300. Don't set too low, as
        image generation takes some time.
    :return: list of responses, one for each text prompt
    :raises: timeout
    """
    logger.info(
        "Incoming call for text-to-image generation with "
        f"engine id {request.engine_id}"
    )
    user_agent = f"droombot/{VERSION}"
    headers = {"Authorization": f"Bearer {STABILITY_API_KEY}", "User-Agent": user_agent}
    url = f"{TEX_TO_IMAGE_BASE_URL}/{request.engine_id}/text-to-image"
    logger.debug(f"Generated url: {url}")

    # FIXME: need to load json serialized because enums.
    raw_post_data = json.loads(request.json())
    # need to filter out engine_id and sampler if it is none
    post_data = {}
    for k, v in raw_post_data.items():
        if k == "engine_id":
            continue
        if k == "sampler" and v is None:
            continue
        post_data[k] = v

    async with session.post(
        url=url, json=post_data, timeout=timeout, headers=headers
    ) as resp:
        results = await resp.json()
        if resp.status >= 400:
            logger.error(f"Call to Stability errored. Response: {results}")
            raise ValueError("An error occurred")

    # responses are encoded in an 'artifacts' item, but this is NOT
    # mentioned in the docs.
    logger.info("Received a successful response from text-to-image generation.")
    return [TextToImageResponse.from_raw_api(r) for r in results["artifacts"]]


if __name__ == "__main__":
    # for testing
    async def main():
        request = TextToImageRequest(
            text_prompts=[
                {
                    "text": "Green trees in a forest with ferns, oil painting",
                    "weight": 0.5,
                }
            ],
        )
        async with aiohttp.ClientSession() as session:
            results = await text_to_image(session, request)

        print(results)

    asyncio.run(main())
