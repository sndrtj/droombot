import pydantic
import pytest
from droombot.models import TextToImageRequestV2Core, TextToImageResponse


def test_generation_text_prompts_not_defined():
    with pytest.raises(pydantic.ValidationError):
        _ = TextToImageRequestV2Core(
            prompt="",
        )


def test_response_from_raw_api():
    example_response = {"base64": "foo", "finishReason": "SUCCESS", "seed": 0}
    assert TextToImageResponse.from_raw_api(example_response) == TextToImageResponse(
        base64="foo", finish_reason="SUCCESS", seed=0
    )
