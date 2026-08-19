from groq import Groq

from config import settings
from services.llm.base import LLMProvider


class GroqProvider(LLMProvider):
    """
    Groq implementation of the LLMProvider interface.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
    ):
        self.api_key = (
            api_key
            or settings.groq_api_key
        )

        self.model_name = (
            model_name
            or settings.llm_model
        )

        self.client = Groq(
            api_key=self.api_key,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate an answer from the configured Groq model.
        """

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "LLM returned an empty response."
            )

        return content.strip()