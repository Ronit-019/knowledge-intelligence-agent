from dataclasses import dataclass

from langchain_core.documents import Document

from config.settings import settings
from retrieval.vector_store import VectorStore
from services.embedding_service import EmbeddingService


@dataclass(frozen=True)
class RetrievalResult:
    """
    Represents one retrieved piece of evidence.

    semantic_score is the similarity score produced by the
    vector-search layer. It is intentionally kept separate from
    any cross-encoder reranking score.
    """

    document: Document
    semantic_score: float
    rerank_score: float | None = None

    @property
    def score(self) -> float:
        """
        Backward-compatible score property.

        Before reranking, this represents the semantic score.
        After reranking, callers should use rerank_score when
        available.
        """

        if self.rerank_score is not None:
            return self.rerank_score

        return self.semantic_score

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

    @property
    def status(self) -> str:
        return self.document.metadata["status"]


class RetrievalService:
    """
    Version-aware semantic retrieval layer.

    Pipeline:

        Query
          ↓
        Query Embedding
          ↓
        FAISS Candidate Retrieval
          ↓
        Similarity Filtering
          ↓
        Active-Version Filtering
          ↓
        Top-K Evidence
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        similarity_threshold: float = 0.65,
        top_k: int | None = None,
    ):
        if not 0 <= similarity_threshold <= 1:
            raise ValueError(
                "similarity_threshold must be between 0 and 1."
            )

        resolved_top_k = (
            top_k
            if top_k is not None
            else settings.top_k
        )

        if resolved_top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.similarity_threshold = similarity_threshold
        self.top_k = resolved_top_k

    def search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[RetrievalResult]:
        """
        Retrieve relevant, active evidence for a query.

        If top_k is omitted, the configured TOP_K value is used.
        """

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        resolved_top_k = (
            top_k
            if top_k is not None
            else self.top_k
        )

        if resolved_top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        query_embedding = (
            self.embedding_service.embed_text(query)
        )

        # Retrieve additional candidates because some may
        # be removed by similarity or status filtering.
        candidate_k = max(
            resolved_top_k * 3,
            10,
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=candidate_k,
        )

        filtered_results: list[RetrievalResult] = []

        for document, score in results:

            # -------------------------------------------------
            # Similarity filtering
            # -------------------------------------------------

            if score < self.similarity_threshold:
                continue

            # -------------------------------------------------
            # Active document filtering
            # -------------------------------------------------

            status = document.metadata.get(
                "status",
                "",
            ).strip().lower()

            if status != "active":
                continue

            filtered_results.append(
                RetrievalResult(
                    document=document,
                    semantic_score=float(score),
                )
            )

            if len(filtered_results) >= resolved_top_k:
                break

        return filtered_results

    def has_evidence(
        self,
        query: str,
        top_k: int | None = None,
    ) -> bool:
        """
        Check whether sufficient current evidence exists.
        """

        results = self.search(
            query=query,
            top_k=top_k,
        )

        return len(results) > 0