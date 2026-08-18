from dataclasses import dataclass

from services.evidence_selector import EvidenceSelection
from services.answer_generation_service import (
    AnswerGenerationService,
)


@dataclass(frozen=True)
class KnowledgeQueryResult:
    """
    Represents the final result of a knowledge-base query.
    """

    query: str
    answer: str
    grounded: bool
    sources: EvidenceSelection

    @property
    def source_count(self) -> int:
        """
        Return the number of evidence sources used.
        """

        return self.sources.count


class KnowledgeQueryService:
    """
    Orchestrates the complete knowledge query pipeline.

    Flow:

        Query
          ↓
        Retrieval
          ↓
        Evidence Selection
          ↓
        Answer Generation
          ↓
        KnowledgeQueryResult
    """

    def __init__(
        self,
        retrieval_service,
        evidence_selector,
        answer_generation_service: AnswerGenerationService,
    ):
        self.retrieval_service = retrieval_service
        self.evidence_selector = evidence_selector
        self.answer_generation_service = (
            answer_generation_service
        )

    def ask(
        self,
        query: str,
    ) -> KnowledgeQueryResult:
        """
        Answer a user question using the knowledge base.
        """

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        # 1. Retrieve relevant evidence.
        retrieval_results = self.retrieval_service.search(
            query=query,
        )

        # 2. Select the final evidence.
        evidence = self.evidence_selector.select(
            retrieval_results,
        )

        # 3. Generate the grounded answer.
        generated_answer = (
            self.answer_generation_service.generate(
                query=query,
                evidence=evidence,
            )
        )

        # 4. Return the application-level result.
        return KnowledgeQueryResult(
            query=query,
            answer=generated_answer.answer,
            grounded=generated_answer.grounded,
            sources=generated_answer.sources,
        )
