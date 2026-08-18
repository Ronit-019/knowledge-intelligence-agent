from dataclasses import dataclass
from pathlib import Path

from langchain_core.documents import Document

from ingestion.models import KnowledgeDocument
from registry.document_registry import DocumentRegistry
from retrieval.vector_store import VectorStore
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.indexing_service import IndexingService
from services.ingestion_service import IngestionService


@dataclass(frozen=True)
class KnowledgeBase:
    """
    Represents a fully built, ready-to-query knowledge base.
    """

    documents: list[KnowledgeDocument]
    chunks: list[Document]
    vector_store: VectorStore
    indexed_documents: int
    embedding_dimension: int


class KnowledgeBaseService:
    """
    Orchestrates the complete knowledge-base construction pipeline.

    Pipeline:

        PDFs
          ↓
        Ingestion
          ↓
        Document Registry
          ↓
        Active Document Resolution
          ↓
        Chunking
          ↓
        Embeddings
          ↓
        Vector Store
    """

    def __init__(
        self,
        ingestion_service: IngestionService,
        document_registry: DocumentRegistry,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
    ):
        self.ingestion_service = ingestion_service
        self.document_registry = document_registry
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service

    def build(
        self,
        knowledge_base_path: str | Path,
    ) -> KnowledgeBase:
        """
        Build a knowledge base using only active document versions.
        """

        # ---------------------------------------------------------
        # 1. Ingest all PDFs
        # ---------------------------------------------------------

        documents = self.ingestion_service.ingest(
            knowledge_base_path
        )

        if not documents:
            raise ValueError(
                "No documents were ingested."
            )

        # ---------------------------------------------------------
        # 2. Register all document versions
        # ---------------------------------------------------------

        self.document_registry.register_many(
            documents
        )

        # ---------------------------------------------------------
        # 3. Resolve active versions
        # ---------------------------------------------------------

        active_documents = (
            self.document_registry.get_active_documents()
        )

        if not active_documents:
            raise ValueError(
                "No active documents available."
            )

        # ---------------------------------------------------------
        # 4. Chunk ONLY active documents
        # ---------------------------------------------------------

        active_chunks = (
            self.chunking_service.chunk_documents(
                active_documents
            )
        )

        if not active_chunks:
            raise ValueError(
                "No chunks were created from active documents."
            )

        # ---------------------------------------------------------
        # 5. Create vector store
        # ---------------------------------------------------------

        vector_store = VectorStore(
            dimension=self.embedding_service.dimension
        )

        # ---------------------------------------------------------
        # 6. Index ONLY active chunks
        # ---------------------------------------------------------

        indexing_service = IndexingService(
            embedding_service=self.embedding_service,
            vector_store=vector_store,
        )

        indexing_result = indexing_service.index(
            active_chunks
        )

        # ---------------------------------------------------------
        # 7. Return ready-to-query knowledge base
        # ---------------------------------------------------------

        return KnowledgeBase(
            documents=active_documents,
            chunks=active_chunks,
            vector_store=vector_store,
            indexed_documents=(
                indexing_result.documents_indexed
            ),
            embedding_dimension=(
                indexing_result.embedding_dimension
            ),
        )