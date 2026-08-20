from dataclasses import dataclass
from pathlib import Path

from config import settings
from ingestion.chunker import DocumentChunker
from ingestion.normalizer import DocumentNormalizer
from registry.document_registry import DocumentRegistry

from services.answer_generation_service import (
    AnswerGenerationService,
)
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.evidence_selector import EvidenceSelector
from services.ingestion_service import IngestionService
from services.knowledge_base_service import (
    KnowledgeBase,
    KnowledgeBaseService,
)
from services.knowledge_query_service import (
    KnowledgeQueryService,
)
from services.llm.groq_provider import GroqProvider
from services.prompt_builder import PromptBuilder
from services.reranking_service import RerankingService
from services.retrieval_service import RetrievalService
from services.conversation_service import (
    ConversationContextService,
)

@dataclass(frozen=True)
class KnowledgeApplication:
    """
    Fully initialized knowledge intelligence application.
    """

    knowledge_base: KnowledgeBase
    query_service: KnowledgeQueryService


def build_knowledge_application() -> KnowledgeApplication:
    """
    Build the complete knowledge intelligence application.
    """

    project_root = Path(
        __file__
    ).resolve().parent.parent

    knowledge_base_path = (
        project_root
        / "data"
        / "knowledge_base"
    )

    # ---------------------------------------------------------
    # Ingestion
    # ---------------------------------------------------------

    normalizer = DocumentNormalizer()

    ingestion_service = IngestionService(
        normalizer=normalizer,
    )

    # ---------------------------------------------------------
    # Registry
    # ---------------------------------------------------------

    document_registry = DocumentRegistry()

    # ---------------------------------------------------------
    # Chunking
    # ---------------------------------------------------------

    chunker = DocumentChunker()

    chunking_service = ChunkingService(
        chunker=chunker,
    )

    # ---------------------------------------------------------
    # Embeddings
    # ---------------------------------------------------------

    embedding_service = EmbeddingService(
        model_name=settings.embedding_model,
    )

    # ---------------------------------------------------------
    # Knowledge Base
    # ---------------------------------------------------------

    knowledge_base_service = KnowledgeBaseService(
        ingestion_service=ingestion_service,
        document_registry=document_registry,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
    )

    knowledge_base = knowledge_base_service.build(
        knowledge_base_path
    )

    # ---------------------------------------------------------
    # Retrieval
    # ---------------------------------------------------------

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=knowledge_base.vector_store,
        top_k=settings.top_k,
    )

    # ---------------------------------------------------------
    # Cross-Encoder Reranking
    # ---------------------------------------------------------

    reranking_service = RerankingService(
        top_k=settings.rerank_top_k,
        min_rerank_score=settings.min_rerank_score,
        enabled=settings.enable_reranking,
    )

    # ---------------------------------------------------------
    # Evidence Selection
    # ---------------------------------------------------------

    evidence_selector = EvidenceSelector()

    # ---------------------------------------------------------
    # LLM Answer Generation
    # ---------------------------------------------------------

    llm_provider = GroqProvider(
        api_key=settings.groq_api_key,
        model_name=settings.llm_model,
    )

    conversation_context_service = (
        ConversationContextService(
            llm_provider=llm_provider,
        )
    )

    prompt_builder = PromptBuilder()

    answer_generation_service = AnswerGenerationService(
        llm_provider=llm_provider,
        prompt_builder=prompt_builder,
    )

    # ---------------------------------------------------------
    # Query Service
    # ---------------------------------------------------------

    query_service = KnowledgeQueryService(
        retrieval_service=retrieval_service,
        evidence_selector=evidence_selector,
        answer_generation_service=answer_generation_service,
        reranking_service=reranking_service,
        conversation_context_service=conversation_context_service,
    )

    return KnowledgeApplication(
        knowledge_base=knowledge_base,
        query_service=query_service,
    )