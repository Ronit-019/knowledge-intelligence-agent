from dataclasses import dataclass

from services.evidence_selector import EvidenceSelection
from services.llm.base import LLMProvider
from services.prompt_builder import PromptBuilder


@dataclass(frozen=True)
class GeneratedAnswer:
    """
    Represents the final answer generated from selected evidence.
    """

    query: str
    answer: str
    grounded: bool
    sources: EvidenceSelection

    @property
    def source_count(self) -> int:
        return self.sources.count


class AnswerGenerationService:
    """
    Generates grounded answers using an LLM.

    The LLM receives only evidence selected by the
    retrieval and reranking pipeline.
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
        history=None,
    ) -> GeneratedAnswer:

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        # -----------------------------------------------------
        # No evidence = abstain
        # -----------------------------------------------------

        if evidence.count == 0:
            return GeneratedAnswer(
                query=query,
                answer=(
                    "I couldn't find enough reliable information "
                    "in the available documents to answer this question."
                ),
                grounded=False,
                sources=evidence,
            )

        # -----------------------------------------------------
        # Build grounded prompt
        # -----------------------------------------------------

        prompt = self.prompt_builder.build(
            query=query,
            evidence=evidence,
            history=history,
        )

        # -----------------------------------------------------
        # Generate answer
        # -----------------------------------------------------

        answer = self.llm_provider.generate(
            prompt
        )

        answer = answer.strip()

        if not answer:
            return GeneratedAnswer(
                query=query,
                answer=(
                    "I couldn't generate a reliable answer "
                    "from the available evidence."
                ),
                grounded=False,
                sources=evidence,
            )

        return GeneratedAnswer(
            query=query,
            answer=answer,
            grounded=True,
            sources=evidence,
        )