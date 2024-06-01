import pydantic
import pytest
from droombot.models import (
    PubSubMessage,
    TextToImageRequestV2Core,
    TextToImageRequestV2SD3,
    TextToImageResponse,
    pubsub_to_t2i,
)


def test_generation_text_prompts_not_defined():
    with pytest.raises(pydantic.ValidationError):
        _ = TextToImageRequestV2Core(
            prompt="",
        )


def test_response_from_raw_api():
    example_response = {"image": "foo", "finish_reason": "SUCCESS", "seed": 0}
    assert TextToImageResponse.from_raw_api(example_response) == TextToImageResponse(
        base64="foo", finish_reason="SUCCESS", seed=0
    )


PUBSUB_TO_T2I_DATA = [
    (
        PubSubMessage(interaction_id="0", text_prompt="foo bar"),
        TextToImageRequestV2Core(prompt="foo bar"),
    ),
    (
        PubSubMessage(interaction_id="0", text_prompt="foo bar -m sd3"),
        TextToImageRequestV2SD3(prompt="foo bar"),
    ),
    (
        PubSubMessage(interaction_id="0", text_prompt="foo bar -m sd3-turbo"),
        TextToImageRequestV2SD3(prompt="foo bar", model="sd3-turbo"),
    ),
    (
        PubSubMessage(interaction_id="0", text_prompt="foo bar --model sd3"),
        TextToImageRequestV2SD3(prompt="foo bar"),
    ),
]


@pytest.mark.parametrize("message, t2i_request", PUBSUB_TO_T2I_DATA)
def test_request_from_pubsub(message, t2i_request):
    assert pubsub_to_t2i(message) == t2i_request
