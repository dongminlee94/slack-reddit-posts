"""Client for Google Generative AI API interaction."""

from google import genai
from google.genai.types import GenerateContentConfig


class GenAIClient:
    """Handler for communication with the Google Generative AI service."""

    def __init__(self, api_key: str, model: str, response_mime_type: str) -> None:
        """Initialize the GenAI client with API key, model, and response type."""
        self._client = genai.Client(api_key=api_key)
        self._model = model
        self._response_mime_type = response_mime_type

    def create_content(self, contents: list[str], system_instruction: str) -> str | None:
        """Generate content using the specified model, content, and system instruction."""
        response = self._client.models.generate_content(
            model=self._model,
            contents=contents,
            config=GenerateContentConfig(
                system_instruction=system_instruction, response_mime_type=self._response_mime_type
            ),
        )

        return response.text
