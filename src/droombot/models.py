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

import enum
import sys
from typing import Annotated, Literal

# See https://docs.pydantic.dev/2.7/errors/usage_errors/#typed-dict-version
if sys.version_info < (3, 12):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict

import pydantic

EngineId = Literal[
    "Stable Diffusion v1.4",
    "stable-diffusion-v1-5",
    "stable-diffusion-512-v2-0",
    "stable-diffusion-768-v2-0",
    "stable-diffusion-512-v2-1",
    "stable-diffusion-768-v2-1",
]


class TextPrompt(TypedDict):
    text: str
    weight: float


class ClipGuidancePreset(enum.Enum):
    NONE = "NONE"
    FAST_BLUE = "FAST_BLUE"
    FAST_GREEN = "FAST_GREEN"
    SIMPLE = "SIMPLE"
    SLOW = "SLOW"
    SLOWER = "SLOWER"
    SLOWEST = "SLOWEST"


class Sampler(enum.Enum):
    DDIM = "DDIM"
    DDPM = "DDPM"
    K_DPMPP_2M = "K_DPMPP_2M"
    K_DPMPP_2S_ANCESTRAL = "K_DPMPP_2S_ANCESTRAL"
    K_DPM_2 = "K_DPM_2"
    K_DPM_2_ANCESTRAL = "K_DPM_2_ANCESTRAL"
    K_EULER = "K_EULER"
    K_EULER_ANCESTRAL = "K_EULER_ANCESTRAL"
    K_HEUN = "K_HEUN"
    K_LMS = "K_LMS"


class FinishReason(enum.Enum):
    CONTENT_FILTERED = "CONTENT_FILTERED"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


SizeType = Annotated[int, pydantic.Field(multiple_of=64, ge=128)]
CfgScaleType = Annotated[int, pydantic.Field(ge=0, le=35)]
SeedType = Annotated[int, pydantic.Field(ge=0, le=4294967295)]
StepsType = Annotated[int, pydantic.Field(ge=10, le=150)]


# Docs: https://platform.stability.ai/rest-api#tag/v1generation/operation/textToImage
class TextToImageRequest(pydantic.BaseModel):
    engine_id: EngineId = "stable-diffusion-512-v2-1"

    height: SizeType = 512
    width: SizeType = 512

    text_prompts: Annotated[list[TextPrompt], pydantic.Field(min_length=1)]
    cfg_scale: CfgScaleType = 7
    clip_guidance_present: ClipGuidancePreset = ClipGuidancePreset.NONE

    # None should indicate omit from api call
    sampler: Sampler | None = None

    # 0 = random
    seed: SeedType = 0

    # number of diffusion steps
    steps: StepsType = 50

    @pydantic.model_validator(mode="after")
    def image_size_must_be_within_bounds(self) -> "TextToImageRequest":
        engine_id = self.engine_id
        height = self.height
        width = self.width

        image_size = height * width

        if "768" in engine_id:
            min_bound = 589_824
        else:
            min_bound = 262_144

        if min_bound <= image_size <= 1_048_576:
            return self

        raise ValueError(f"Image size {image_size} is out of bounds.")


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
            base64=raw_api_response["base64"],
            finish_reason=raw_api_response["finishReason"],
            seed=raw_api_response["seed"],
        )


class PubSubMessage(pydantic.BaseModel):
    """Message used for passing in pub/sub"""

    # the discord interaction id
    interaction_id: str

    # The text prompt used
    text_prompt: str
