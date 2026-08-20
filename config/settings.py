import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """
    Central application configuration.

    Configuration is loaded from environment variables with
    sensible defaults for local development.
    """

    def __init__(self):
        self.groq_api_key = self._required(
            "GROQ_API_KEY"
        )

        self.llm_provider = os.getenv(
            "LLM_PROVIDER",
            "groq",
        )

        self.llm_model = os.getenv(
            "LLM_MODEL",
            "openai/gpt-oss-20b",
        )

        self.embedding_model = os.getenv(
            "EMBEDDING_MODEL",
            "BAAI/bge-small-en-v1.5",
        )

        self.top_k = self._positive_int(
            "TOP_K",
            10,
        )

        self.rerank_top_k = self._positive_int(
            "RERANK_TOP_K",
            5,
        )

        self.environment = os.getenv(
            "ENVIRONMENT",
            "development",
        )

        self.log_level = os.getenv(
            "LOG_LEVEL",
            "INFO",
        )
        self.min_rerank_score = float(
            os.getenv(
                "MIN_RERANK_SCORE",
                "-3.0",
            )
        )

        self.enable_reranking = (
            os.getenv(
                "ENABLE_RERANKING",
                "true",
            ).lower()== "true"
        )

    @staticmethod
    def _required(name: str) -> str:
        value = os.getenv(name)

        if not value or not value.strip():
            raise ValueError(
                f"{name} environment variable is not set."
            )

        return value.strip()

    @staticmethod
    def _positive_int(
        name: str,
        default: int,
    ) -> int:
        value = os.getenv(name)

        if value is None:
            return default

        try:
            parsed = int(value)
        except ValueError as exc:
            raise ValueError(
                f"{name} must be an integer."
            ) from exc

        if parsed <= 0:
            raise ValueError(
                f"{name} must be greater than zero."
            )

        return parsed


settings = Settings()