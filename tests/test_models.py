import pydantic.error_wrappers
import pytest

from droombot.models import GenerationRequest


def test_generation_request_out_of_bounds():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        _ = GenerationRequest(
            engine_id="stable-diffusion-512-v2-0",
            width=2048,
            height=2048,
            text_prompts=[{"text": "A green tree", "weight": "0.5"}],
        )
