import os
from dotenv import load_dotenv
from groq import Groq

from services.llm.base import LLMProvider

load_dotenv()

class GroqProvider(LLMProvider):
    """
    Groq implementation of the LLMProvider interface.
    """

    def __init__(
        self,
        model_name: str = "openai/gpt-oss-20b",
    ):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set."
            )

        self.model_name = model_name

        self.client = Groq(
            api_key=api_key,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

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