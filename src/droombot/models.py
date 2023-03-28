import enum
from typing import Literal, TypedDict, cast

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


# It's 2023, and `pydantic.conint / conlist` still doesn't work nicely with mypy.
# https://github.com/pydantic/pydantic/issues/156
class SizeType(pydantic.ConstrainedInt):
    multiple_of = 64
    ge = 128


class TextPrompts(pydantic.ConstrainedList):
    item_type = TextPrompt
    min_items = 1


class CfgScaleType(pydantic.ConstrainedInt):
    ge = 0
    le = 35


class SeedType(pydantic.ConstrainedInt):
    ge = 0
    le = 4294967295


class StepsType(pydantic.ConstrainedInt):
    ge = 10
    le = 150


# Docs: https://platform.stability.ai/rest-api#tag/v1generation/operation/textToImage
class GenerationRequest(pydantic.BaseModel):
    engine_id: EngineId = "stable-diffusion-512-v2-0"

    height: SizeType = cast(SizeType, 512)
    width: SizeType = cast(SizeType, 512)

    text_prompts: TextPrompts
    cfg_scale: CfgScaleType = cast(CfgScaleType, 7)
    clip_guidance_present: ClipGuidancePreset = ClipGuidancePreset.NONE

    # None should indicate omit from api call
    sampler: Sampler | None = None

    # 0 = random
    seed: SeedType = cast(SeedType, 0)

    # number of diffusion steps
    steps: StepsType = cast(StepsType, 50)

    @pydantic.validator("width")
    def image_size_must_be_within_bounds(cls, v, values, **kwargs):
        # height and width must be between 589,824 and ≤ 1,048,576 if model is 768
        # else between 262,144 and  1,048,576
        engine_id = values["engine_id"]
        height = values["height"]

        image_size = height * v

        if "768" in engine_id:
            min_bound = 589_824
        else:
            min_bound = 262_144

        if min_bound <= image_size <= 1_048_576:
            return v

        raise ValueError(f"Image size {image_size} is out of bounds.")
