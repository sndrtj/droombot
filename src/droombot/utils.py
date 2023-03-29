import base64
import io

from .models import FinishReason, TextToImageResponse


def text_to_image_result_to_buffer(response: TextToImageResponse) -> io.BytesIO:
    if response.finish_reason is not FinishReason.SUCCESS:
        raise ValueError("Need a successful response")

    if response.base64 is None:
        raise ValueError("Need data to generate a buffer")

    buffer = io.BytesIO()
    buffer.write(base64.b64decode(response.base64))
    buffer.seek(0)
    return buffer
