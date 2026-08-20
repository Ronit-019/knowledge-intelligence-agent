from evaluation.models import (
    RetrievalEvaluationResult,
    RetrievalTestCase,
)
from services.retrieval_service import RetrievalService


class RetrievalEvaluator:
    """
    Evaluates retrieval quality against labelled test cases.

    Metrics supported:

    - Recall@K
    - Mean Reciprocal Rank
    - Negative-query abstention accuracy
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

        # -----------------------------------------------------
        # Negative query
        # -----------------------------------------------------

        if test_case.expected_document_id is None:

            abstention_correct = (
                len(results) == 0
            )

            return RetrievalEvaluationResult(
                query=test_case.query,
                expected_document_id=None,
                retrieved_document_ids=retrieved_document_ids,
                retrieved_chunk_ids=retrieved_chunk_ids,
                retrieval_hit=False,
                reciprocal_rank=0.0,
                abstention_correct=abstention_correct,
            )

        # -----------------------------------------------------
        # Positive query
        # -----------------------------------------------------

        retrieval_hit = (
            test_case.expected_document_id
            in retrieved_document_ids
        )

        reciprocal_rank = 0.0

        if retrieval_hit:

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
            retrieved_document_ids=retrieved_document_ids,
            retrieved_chunk_ids=retrieved_chunk_ids,
            retrieval_hit=retrieval_hit,
            reciprocal_rank=reciprocal_rank,
            abstention_correct=False,
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

    @staticmethod
    def calculate_recall(
        results: list[RetrievalEvaluationResult],
    ) -> float:

        positive_cases = [
            result
            for result in results
            if result.is_positive_case
        ]

        if not positive_cases:
            return 0.0

        hits = sum(
            result.retrieval_hit
            for result in positive_cases
        )

        return hits / len(positive_cases)

    @staticmethod
    def calculate_mrr(
        results: list[RetrievalEvaluationResult],
    ) -> float:

        positive_cases = [
            result
            for result in results
            if result.is_positive_case
        ]

        if not positive_cases:
            return 0.0

        return sum(
            result.reciprocal_rank
            for result in positive_cases
        ) / len(positive_cases)

    @staticmethod
    def calculate_abstention_accuracy(
        results: list[RetrievalEvaluationResult],
    ) -> float:

        negative_cases = [
            result
            for result in results
            if not result.is_positive_case
        ]

        if not negative_cases:
            return 0.0

        correct = sum(
            result.abstention_correct
            for result in negative_cases
        )

        return correct / len(negative_cases)