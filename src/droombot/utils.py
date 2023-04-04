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
