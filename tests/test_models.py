import pydantic.error_wrappers
import pytest

from droombot.models import TextToImageRequest, TextToImageResponse


def test_generation_request_out_of_bounds():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        _ = TextToImageRequest(
            engine_id="stable-diffusion-512-v2-0",
            width=2048,
            height=2048,
            text_prompts=[{"text": "A green tree", "weight": "0.5"}],
        )


def test_generation_text_prompts_not_defined():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        _ = TextToImageRequest(
            engine_id="stable-diffusion-512-v2-0",
            width=512,
            height=512,
            text_prompts=[],
        )


def test_response_from_raw_api():
    example_response = {"base64": "foo", "finishReason": "SUCCESS", "seed": 0}
    assert TextToImageResponse.from_raw_api(example_response) == TextToImageResponse(
        base64="foo", finish_reason="SUCCESS", seed=0
    )
