from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalTestCase:
    """
    Represents one query used to evaluate retrieval quality.
    """

    query: str
    expected_document_id: str | None
    expected_chunk_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class RetrievalEvaluationResult:
    """
    Result of evaluating one retrieval query.
    """

    query: str
    expected_document_id: str | None
    retrieved_document_ids: tuple[str, ...]
    retrieved_chunk_ids: tuple[str, ...]
    hit: bool
    reciprocal_rank: float