from dataclasses import dataclass

from langchain_core.documents import Document

from retrieval.vector_store import VectorStore
from services.embedding_service import EmbeddingService


@dataclass(frozen=True)
class RetrievalResult:
    """
    Represents one retrieved piece of evidence.

    Keeps the retrieved document together with its
    similarity score and important source metadata.
    """

    document: Document
    score: float

    @property
    def chunk_id(self) -> str:
        return self.document.metadata["chunk_id"]

    @property
    def document_id(self) -> str:
        return self.document.metadata["document_id"]

    @property
    def title(self) -> str:
        return self.document.metadata["title"]

    @property
    def version(self) -> str:
        return self.document.metadata["version"]

    @property
    def page(self) -> int:
        return self.document.metadata["page"]


class RetrievalService:
    """
    Production retrieval layer.

    Responsibilities:
    - Convert user queries into embeddings
    - Search the vector store
    - Rank relevant chunks
    - Apply similarity thresholds
    - Return traceable evidence
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        similarity_threshold: float = 0.65,
    ):
        if not 0 <= similarity_threshold <= 1:
            raise ValueError(
                "similarity_threshold must be between 0 and 1."
            )

        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve the most relevant evidence for a query.
        """

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        query_embedding = (
            self.embedding_service.embed_text(query)
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        filtered_results = []

        for document, score in results:
            if score >= self.similarity_threshold:
                filtered_results.append(
                    RetrievalResult(
                        document=document,
                        score=score,
                    )
                )

        return filtered_results

    def has_evidence(
        self,
        query: str,
        top_k: int = 5,
    ) -> bool:
        """
        Check whether sufficient evidence exists
        to answer a query.
        """

        results = self.search(
            query=query,
            top_k=top_k,
        )

        return len(results) > 0