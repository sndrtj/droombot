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
import argparse
import enum
import logging
import shlex
from typing import Annotated, Literal

import pydantic

logger = logging.getLogger(__name__)


class FinishReason(enum.Enum):
    CONTENT_FILTERED = "CONTENT_FILTERED"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


ASPECT_RATIOS = Literal["16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "9:16", "9:21"]
STYLE_PRESETS = Literal[
    "3d-model",
    "analog-film",
    "anime",
    "cinematic",
    "comic-book",
    "digital-art",
    "enhance",
    "fantasy-art",
    "isometric",
    "line-art",
    "low-poly",
    "modeling-compound",
    "neon-punk",
    "origami",
    "photographic",
    "pixel-art",
    "tile-texture",
]


SeedType = Annotated[int, pydantic.Field(ge=0, le=4294967295)]
PromptType = Annotated[str, pydantic.Field(min_length=1, max_length=10_000)]
NegativePromptType = Annotated[str, pydantic.Field(min_length=0, max_length=10_000)]


class TextToImageResponse(pydantic.BaseModel):
    # base-64 encoded image or null if finish reason is not success
    base64: str | None
    # the finish reason
    finish_reason: FinishReason
    # What seed ended up being used for this
    seed: int

    @classmethod
    def from_raw_api(cls, raw_api_response: dict) -> "TextToImageResponse":
        return cls(
            base64=raw_api_response["image"],
            finish_reason=raw_api_response["finish_reason"],
            seed=raw_api_response["seed"],
        )


class TextToImageRequestV2Core(pydantic.BaseModel):
    """TextToImage request for the core v2 api of Stability AI"""

    prompt: PromptType
    aspect_ratio: ASPECT_RATIOS = "1:1"
    negative_prompt: NegativePromptType | None = None
    seed: SeedType = 0
    style_preset: STYLE_PRESETS | None = None
    output_format: Literal["jpeg", "png", "webp"] = "png"


class TextToImageRequestV2SD3(pydantic.BaseModel):
    """TextToImage request for the Stable Diffusion 3 api of Stability AI"""

    prompt: PromptType
    aspect_ratio: ASPECT_RATIOS = "1:1"
    negative_prompt: NegativePromptType | None = None
    model: Literal["sd3", "sd3-turbo"] = "sd3"
    seed: SeedType = 0
    output_format: Literal["jpeg", "png"] = "png"


class PubSubMessage(pydantic.BaseModel):
    """Message used for passing in pub/sub"""

    # the discord interaction id
    interaction_id: str

    # The text prompt used
    text_prompt: str


def pubsub_to_t2i(
    message: PubSubMessage,
) -> TextToImageRequestV2Core | TextToImageRequestV2SD3:
    """Convert a pubsub message to a text 2 image request

    :param message: the message
    :return: text to image request
    """
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument(
        "-m", "--model", choices=["core", "sd3", "sd3-turbo"], default="core"
    )

    # we want to consider everything before a `-` as the text prompt, without quoting.
    prompt, maybe_dash, options = message.text_prompt.partition("-")

    args, failures = parser.parse_known_args(shlex.split(maybe_dash + options), None)
    if failures:
        logger.warning(f"Unrecognized arguments: {''.join(failures)}, ignoring...")

    if args.model == "core":
        return TextToImageRequestV2Core(prompt=prompt.strip())

    return TextToImageRequestV2SD3(prompt=prompt.strip(), model=args.model)
