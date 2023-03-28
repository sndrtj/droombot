import asyncio
import json
import os

import aiohttp

from .models import TextToImageRequest, TextToImageResponse

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
    # note, this is blocking
    stability_api_key = os.getenv("STABILITY_API_KEY")
    headers = {"Authorization": f"Bearer {stability_api_key}"}
    url = f"{TEX_TO_IMAGE_BASE_URL}/{request.engine_id}/text-to-image"

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
            print(results)
            raise ValueError("An error occurred")

    # responses are encoded in an 'artifacts' item, but this is NOT
    # mentioned in the docs.
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
