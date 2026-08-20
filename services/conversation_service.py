from dataclasses import dataclass

from services.llm.base import LLMProvider


@dataclass(frozen=True)
class ConversationMessage:
    role: str
    content: str


class ConversationContextService:
    """
    Converts a conversational follow-up question into a
    self-contained retrieval query.

    Conversation history is used only for query understanding.
    It is NOT treated as factual evidence.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
    ):
        self.llm_provider = llm_provider

    def contextualize(
        self,
        query: str,
        history: list[ConversationMessage] | None = None,
    ) -> str:

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if not history:
            return query

        recent_history = history[-6:]

        history_text = "\n".join(
            f"{message.role.upper()}: {message.content}"
            for message in recent_history
        )

        prompt = f"""
Rewrite the user's latest question into a standalone
knowledge-base search query.

Use the conversation only to resolve references such as:
- it
- that
- this
- they
- the policy
- the above
- that period
- that requirement

Do not answer the question.

Do not add facts.

If the latest question is already standalone,
return it unchanged.

CONVERSATION:
{history_text}

LATEST USER QUESTION:
{query}

STANDALONE SEARCH QUERY:
""".strip()

        contextualized = self.llm_provider.generate(prompt).strip()

        return contextualized or query