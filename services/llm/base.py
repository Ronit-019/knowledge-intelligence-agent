from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """
    Abstract interface for language-model providers.

    The application depends on this interface rather than
    depending directly on a specific LLM provider.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response from the supplied prompt.

        Implementations must return the generated text.
        """
        raise NotImplementedError