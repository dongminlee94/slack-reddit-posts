"""Client for Google Generative AI API interaction."""

import secrets
import time

from google import genai
from google.genai.errors import APIError
from google.genai.types import GenerateContentConfig, GenerateContentResponse
from httpx import RemoteProtocolError, TimeoutException


class GenAIClient:
    """Handler for communication with the Google Generative AI service."""

    def __init__(self, api_key: str, model: str, response_mime_type: str) -> None:
        """Initialize the GenAI client with API key, model, and response type."""
        self._client = genai.Client(api_key=api_key)
        self._model = model
        self._response_mime_type = response_mime_type

    def _generate_content(
        self,
        contents: list[str],
        system_instruction: str,
        temperature: float,
        top_p: float,
    ) -> GenerateContentResponse:
        """Generate content using the specified model, content, and system instruction."""
        return self._client.models.generate_content(
            model=self._model,
            contents=contents,
            config=GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                top_p=top_p,
                response_mime_type=self._response_mime_type,
            ),
        )

    def generate_content_with_retry(
        self,
        contents: list[str],
        system_instruction: str,
        temperature: float,
        top_p: float,
        max_retries: int = 5,
        backoff_factor: int = 3,
        initial_delay: int = 1,
    ) -> GenerateContentResponse:
        """Generate content with a retry mechanism for transient errors."""
        for attempt in range(max_retries + 1):
            try:
                return self._generate_content(
                    contents=contents,
                    system_instruction=system_instruction,
                    temperature=temperature,
                    top_p=top_p,
                )

            except (APIError, RemoteProtocolError, TimeoutException) as e:
                if attempt == max_retries:
                    raise RuntimeError(f"Max retries reached. Error: {e}") from e

                delay = initial_delay * (backoff_factor**attempt) + secrets.SystemRandom().uniform(0, 1)
                time.sleep(delay)
            except Exception as e:
                raise e

        raise RuntimeError("Retry loop completed without returning a response or raising a specific error.")
