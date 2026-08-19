from dataclasses import dataclass

from services.answer_generation_service import (
    GeneratedAnswer,
)
from services.evidence_selector import EvidenceSelection
from services.knowledge_query_service import (
    KnowledgeQueryService,
)


@dataclass
class FakeRetrievalService:
    results: list

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):
        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        return self.results


class FakeEvidenceSelector:

    def select(
        self,
        results,
    ):
        return EvidenceSelection(
            results=results
        )


class FakeAnswerGenerationService:

    def __init__(self):
        self.received_query = None
        self.received_evidence = None

    def generate(
        self,
        query,
        evidence,
    ):
        self.received_query = query
        self.received_evidence = evidence

        if evidence.count == 0:
            return GeneratedAnswer(
                query=query,
                answer=(
                    "I couldn't find enough information "
                    "in the available documents to answer "
                    "this question."
                ),
                grounded=False,
                sources=evidence,
            )

        return GeneratedAnswer(
            query=query,
            answer=(
                "The employee may work internationally "
                "for up to 90 days."
            ),
            grounded=True,
            sources=evidence,
        )


def build_service(results):
    retrieval_service = FakeRetrievalService(
        results=results
    )

    evidence_selector = FakeEvidenceSelector()

    answer_generation_service = (
        FakeAnswerGenerationService()
    )

    service = KnowledgeQueryService(
        retrieval_service=retrieval_service,
        evidence_selector=evidence_selector,
        answer_generation_service=answer_generation_service,
    )

    return (
        service,
        answer_generation_service,
    )


def test_supported_query():
    fake_result = object()

    service, generator = build_service(
        [fake_result]
    )

    query = (
        "How long can an employee work from another country?"
    )

    result = service.ask(query)

    assert result.query == query

    assert result.answer == (
        "The employee may work internationally "
        "for up to 90 days."
    )

    assert result.grounded is True
    assert result.source_count == 1

    assert generator.received_query == query

    assert (
        generator.received_evidence
        is result.sources
    )


def test_empty_evidence():
    service, generator = build_service([])

    query = "What is the maternity leave policy?"

    result = service.ask(query)

    assert result.query == query
    assert result.grounded is False
    assert result.source_count == 0

    assert (
        "couldn't find enough information"
        in result.answer
    )

    assert generator.received_query == query

    assert (
        generator.received_evidence.count == 0
    )


def test_empty_query():
    service, _ = build_service([])

    try:
        service.ask("   ")

        raise AssertionError(
            "Empty query should have been rejected."
        )

    except ValueError as exc:
        assert str(exc) == "Query cannot be empty."


def main():
    print("=" * 70)
    print("KNOWLEDGE QUERY SERVICE")
    print("=" * 70)

    print()
    print("-" * 70)
    print("SUPPORTED QUERY")
    print("-" * 70)

    test_supported_query()

    print("Query orchestration: OK")
    print("Grounded response: OK")
    print("Source metadata: OK")

    print()
    print("-" * 70)
    print("EMPTY EVIDENCE")
    print("-" * 70)

    test_empty_evidence()

    print("Ungrounded response: OK")
    print("Zero sources handled correctly: OK")

    print()
    print("-" * 70)
    print("EMPTY QUERY")
    print("-" * 70)

    test_empty_query()

    print("Empty query correctly rejected.")

    print()
    print("=" * 70)
    print("KNOWLEDGE QUERY SERVICE PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()