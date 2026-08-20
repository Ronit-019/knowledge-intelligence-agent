from sentence_transformers import CrossEncoder

from config.settings import settings
from services.retrieval_service import RetrievalResult


class RerankingService:
    """
    Reranks semantic-retrieval candidates using a cross-encoder.
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_k: int | None = None,
        min_rerank_score: float | None = None,
    ):
        resolved_top_k = (
            top_k
            if top_k is not None
            else settings.rerank_top_k
        )

        resolved_min_rerank_score = (
            min_rerank_score
            if min_rerank_score is not None
            else settings.min_rerank_score
        )

        if resolved_top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        self.model_name = model_name
        self.top_k = resolved_top_k
        self.min_rerank_score = resolved_min_rerank_score

        self.model = CrossEncoder(
            self.model_name
        )

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int | None = None,
    ) -> list[RetrievalResult]:
        """
        Rerank retrieval candidates.

        The original semantic score is preserved.
        The cross-encoder score is stored separately as
        rerank_score.
        """

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        if not results:
            return []

        resolved_top_k = (
            top_k
            if top_k is not None
            else self.top_k
        )

        if resolved_top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        pairs = [
            (
                query,
                result.document.page_content,
            )
            for result in results
        ]

        scores = self.model.predict(
            pairs
        )

        reranked = [
            RetrievalResult(
                document=result.document,
                semantic_score=result.semantic_score,
                rerank_score=float(score),
            )
            for result, score in zip(
                results,
                scores,
            )
        ]
        reranked.sort(
            key=lambda result: (
                result.rerank_score
                if result.rerank_score is not None
                else float("-inf")
            ),
            reverse=True,
        )

        reranked = [
            result
            for result in reranked
            if (
                result.rerank_score is not None
                and result.rerank_score >= self.min_rerank_score
            )
        ]

        return reranked[:resolved_top_k]