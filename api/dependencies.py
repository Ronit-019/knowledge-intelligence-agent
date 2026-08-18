from pathlib import Path

from ingestion.chunker import DocumentChunker
from ingestion.normalizer import DocumentNormalizer
from registry.document_registry import DocumentRegistry

from services.answer_generation_service import AnswerGenerationService
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.evidence_selector import EvidenceSelector
from services.ingestion_service import IngestionService
from services.knowledge_base_service import KnowledgeBaseService
from services.knowledge_query_service import KnowledgeQueryService
from services.prompt_builder import PromptBuilder
from services.retrieval_service import RetrievalService
from services.llm.groq_provider import GroqProvider


def build_knowledge_query_service() -> KnowledgeQueryService:
    """
    Build the complete knowledge-query application pipeline.
    """

    knowledge_base_path = Path(
        "data/knowledge_base"
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

    embedding_service = EmbeddingService()

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
    )

    # ---------------------------------------------------------
    # Evidence selection
    # ---------------------------------------------------------

    evidence_selector = EvidenceSelector()

    # ---------------------------------------------------------
    # Answer generation
    # ---------------------------------------------------------

    llm_provider = GroqProvider()

    prompt_builder = PromptBuilder()

    answer_generation_service = AnswerGenerationService(
        llm_provider=llm_provider,
        prompt_builder=prompt_builder,
    )

    # ---------------------------------------------------------
    # Application query service
    # ---------------------------------------------------------

    return KnowledgeQueryService(
        retrieval_service=retrieval_service,
        evidence_selector=evidence_selector,
        answer_generation_service=answer_generation_service,
    )
