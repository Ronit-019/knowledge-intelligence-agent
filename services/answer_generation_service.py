from dataclasses import dataclass

from services.evidence_selector import EvidenceSelection
from services.llm.base import LLMProvider
from services.prompt_builder import PromptBuilder


@dataclass(frozen=True)
class GeneratedAnswer:
    """
    Represents the final answer generated from selected evidence.
    """

    answer: str
    grounded: bool
    sources: EvidenceSelection


class AnswerGenerationService:
    """
    Generates grounded answers using an LLM.

    The LLM receives only evidence selected by the
    retrieval pipeline.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        prompt_builder: PromptBuilder,
    ):
        self.llm_provider = llm_provider
        self.prompt_builder = prompt_builder

    def generate(
        self,
        query: str,
        evidence: EvidenceSelection,
    ) -> GeneratedAnswer:

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        if evidence.count == 0:
            return GeneratedAnswer(
                answer=(
                    "I couldn't find enough information in the "
                    "available documents to answer this question."
                ),
                grounded=False,
                sources=evidence,
            )

        prompt = self.prompt_builder.build(
            query=query,
            evidence=evidence,
        )

        answer = self.llm_provider.generate(
            prompt
        )

        return GeneratedAnswer(
            answer=answer,
            grounded=True,
            sources=evidence,
        )