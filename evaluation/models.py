from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalTestCase:
    """
    Represents one query used to evaluate retrieval quality.
    """

    query: str

    # Document that should contain the answer.
    # None means the query should be rejected as unanswerable.
    expected_document_id: str | None

    # Optional exact chunks that are expected to contain
    # the relevant evidence.
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

    retrieval_hit: bool
    reciprocal_rank: float

    # For unanswerable queries:
    # True when the system correctly returned no evidence.
    abstention_correct: bool

    @property
    def is_positive_case(self) -> bool:
        return self.expected_document_id is not None