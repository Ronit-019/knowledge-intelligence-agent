from services.answer_generation_service import (
    AnswerGenerationService,
)
from services.conversation_service import (
    ConversationContextService,
    ConversationMessage,
)
from services.evidence_selector import (
    EvidenceSelector,
)
from services.retrieval_service import (
    RetrievalService,
)
from services.reranking_service import (
    RerankingService,
)


class KnowledgeQueryService:
    """
    Orchestrates the complete knowledge-query pipeline.

    Pipeline:

        Conversation
              ↓
        Query contextualization
              ↓
        Semantic Retrieval
              ↓
        Cross-Encoder Reranking
              ↓
        Evidence Selection
              ↓
        Grounded Answer Generation
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        evidence_selector: EvidenceSelector,
        answer_generation_service: AnswerGenerationService,
        reranking_service: RerankingService | None = None,
        conversation_context_service: ConversationContextService | None = None,
    ):
        self.retrieval_service = retrieval_service
        self.evidence_selector = evidence_selector
        self.answer_generation_service = (
            answer_generation_service
        )
        self.reranking_service = reranking_service
        self.conversation_context_service = (
            conversation_context_service
        )

    def ask(
        self,
        query: str,
        history: list[ConversationMessage] | None = None,
    ):
        """
        Answer a question using conversation context,
        retrieved evidence, reranking and grounded generation.
        """

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        history = history or []

        # -----------------------------------------------------
        # 1. Contextualize conversational query
        # -----------------------------------------------------

        retrieval_query = query

        if self.conversation_context_service is not None:
            retrieval_query = (
                self.conversation_context_service.contextualize(
                    query=query,
                    history=history,
                )
            )

        # -----------------------------------------------------
        # 2. Semantic retrieval
        # -----------------------------------------------------

        retrieval_results = (
            self.retrieval_service.search(
                query=retrieval_query,
            )
        )

        # -----------------------------------------------------
        # 3. Cross-encoder reranking
        # -----------------------------------------------------

        if self.reranking_service is not None:
            retrieval_results = (
                self.reranking_service.rerank(
                    query=retrieval_query,
                    results=retrieval_results,
                )
            )

        # -----------------------------------------------------
        # 4. Evidence selection
        # -----------------------------------------------------

        evidence = self.evidence_selector.select(
            retrieval_results
        )

        # -----------------------------------------------------
        # 5. Grounded answer generation
        # -----------------------------------------------------

        return self.answer_generation_service.generate(
            query=query,
            evidence=evidence,
            history=history,
        )