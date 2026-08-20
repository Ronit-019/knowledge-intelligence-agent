from langchain_core.documents import Document

from services.retrieval_service import RetrievalResult
from services.reranking_service import RerankingService


def build_result(
    chunk_id: str,
    content: str,
    score: float,
) -> RetrievalResult:

    document = Document(
        page_content=content,
        metadata={
            "chunk_id": chunk_id,
            "document_id": "TEST-001",
            "title": "Test Policy",
            "version": "1.0",
            "page": 1,
            "status": "active",
        },
    )

    return RetrievalResult(
        document=document,
        semantic_score=score,
    )


def main():

    print("=" * 70)
    print("CROSS-ENCODER RERANKING")
    print("=" * 70)

    query = (
        "How long can an employee work from another country?"
    )

    results = [
        build_result(
            chunk_id="chunk-1",
            content=(
                "Employees may work remotely from their "
                "primary residence with manager approval."
            ),
            score=0.70,
        ),
        build_result(
            chunk_id="chunk-2",
            content=(
                "International remote work may be approved "
                "for up to 90 consecutive calendar days."
            ),
            score=0.69,
        ),
        build_result(
            chunk_id="chunk-3",
            content=(
                "Employees must complete security training "
                "before accessing company systems."
            ),
            score=0.68,
        ),
    ]

    reranker = RerankingService(
        top_k=2,
    )

    reranked = reranker.rerank(
        query=query,
        results=results,
    )

    print("\n" + "-" * 70)
    print("RERANKED RESULTS")
    print("-" * 70)

    for rank, result in enumerate(
        reranked,
        start=1,
    ):
        print(f"\nRank: {rank}")
        print(
            f"Semantic score: "
            f"{result.semantic_score:.4f}"
        )
        print(
            f"Rerank score: "
            f"{result.rerank_score:.4f}"
        )
        print(
            f"Chunk: "
            f"{result.chunk_id}"
        )
        print(
            f"Content: "
            f"{result.document.page_content}"
        )

    # ---------------------------------------------------------
    # Result count
    # ---------------------------------------------------------

    assert len(reranked) == 2

    # ---------------------------------------------------------
    # Relevant result should rank first
    # ---------------------------------------------------------

    assert (
        reranked[0].chunk_id == "chunk-2"
    )

    # ---------------------------------------------------------
    # Original semantic scores must be preserved
    # ---------------------------------------------------------

    semantic_scores = {
        result.chunk_id: result.semantic_score
        for result in reranked
    }

    assert (
        semantic_scores["chunk-2"] == 0.69
    )

    # ---------------------------------------------------------
    # Cross-encoder scores must exist separately
    # ---------------------------------------------------------

    assert (
        reranked[0].rerank_score is not None
    )

    assert (
        reranked[1].rerank_score is not None
    )

    # The generic score property should expose the
    # reranking score once reranking has occurred.
    assert (
        reranked[0].score
        == reranked[0].rerank_score
    )

    print("\n" + "=" * 70)
    print("RERANKING TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()