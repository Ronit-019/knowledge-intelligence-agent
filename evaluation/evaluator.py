from evaluation.models import (
    RetrievalEvaluationResult,
    RetrievalTestCase,
)
from services.retrieval_service import RetrievalService


class RetrievalEvaluator:
    """
    Evaluates retrieval quality against labelled test cases.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ):
        self.retrieval_service = retrieval_service

    def evaluate_case(
        self,
        test_case: RetrievalTestCase,
        top_k: int = 5,
    ) -> RetrievalEvaluationResult:
        results = self.retrieval_service.search(
            query=test_case.query,
            top_k=top_k,
        )

        retrieved_document_ids = tuple(
            result.document_id
            for result in results
        )

        retrieved_chunk_ids = tuple(
            result.chunk_id
            for result in results
        )

        if test_case.expected_document_id is None:
            hit = len(results) == 0
            reciprocal_rank = 0.0

        else:
            hit = (
                test_case.expected_document_id
                in retrieved_document_ids
            )

            reciprocal_rank = 0.0

            if hit:
                rank = (
                    retrieved_document_ids.index(
                        test_case.expected_document_id
                    )
                    + 1
                )

                reciprocal_rank = 1.0 / rank

        return RetrievalEvaluationResult(
            query=test_case.query,
            expected_document_id=(
                test_case.expected_document_id
            ),
            retrieved_document_ids=(
                retrieved_document_ids
            ),
            retrieved_chunk_ids=(
                retrieved_chunk_ids
            ),
            hit=hit,
            reciprocal_rank=reciprocal_rank,
        )

    def evaluate(
        self,
        test_cases: list[RetrievalTestCase],
        top_k: int = 5,
    ) -> list[RetrievalEvaluationResult]:
        return [
            self.evaluate_case(
                test_case=test_case,
                top_k=top_k,
            )
            for test_case in test_cases
        ]