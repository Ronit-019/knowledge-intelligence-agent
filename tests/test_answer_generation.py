from langchain_core.documents import Document

from services.answer_generation_service import (
    AnswerGenerationService,
)
from services.evidence_selector import EvidenceSelection
from services.llm.base import LLMProvider
from services.prompt_builder import PromptBuilder
from services.retrieval_service import RetrievalResult


class FakeLLMProvider(LLMProvider):
    """
    Deterministic LLM provider for unit testing.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:
        return (
            "International remote work may be approved "
            "for up to 90 consecutive calendar days."
        )


def build_evidence() -> EvidenceSelection:
    document = Document(
        page_content=(
            "International remote work may be approved "
            "for up to 90 consecutive calendar days."
        ),
        metadata={
            "chunk_id": "HR-RW-001:2.0:1:0",
            "document_id": "HR-RW-001",
            "title": "Remote Work Policy",
            "version": "2.0",
            "page": 1,
        },
    )

    result = RetrievalResult(
        document=document,
        score=0.7347,
    )

    return EvidenceSelection(
        results=[result]
    )


def main():
    print("=" * 70)
    print("ANSWER GENERATION")
    print("=" * 70)

    prompt_builder = PromptBuilder()

    service = AnswerGenerationService(
        llm_provider=FakeLLMProvider(),
        prompt_builder=prompt_builder,
    )

    # ---------------------------------------------------------
    # SUPPORTED QUERY
    # ---------------------------------------------------------

    print("\n")
    print("-" * 70)
    print("SUPPORTED QUERY")
    print("-" * 70)

    evidence = build_evidence()

    generated = service.generate(
        query=(
            "How long can an employee work "
            "from another country?"
        ),
        evidence=evidence,
    )

    print("\nAnswer:")
    print(generated.answer)

    print("\nGrounded:", generated.grounded)
    print("Sources:", generated.sources.count)

    assert generated.grounded is True
    assert generated.sources.count == 1

    assert (
        "90 consecutive calendar days"
        in generated.answer
    )

    # ---------------------------------------------------------
    # UNSUPPORTED QUERY
    # ---------------------------------------------------------

    print("\n")
    print("-" * 70)
    print("UNSUPPORTED QUERY")
    print("-" * 70)

    empty_evidence = EvidenceSelection(
        results=[]
    )

    generated = service.generate(
        query=(
            "What is the company's maternity "
            "leave policy?"
        ),
        evidence=empty_evidence,
    )

    print("\nAnswer:")
    print(generated.answer)

    print("\nGrounded:", generated.grounded)
    print("Sources:", generated.sources.count)

    assert generated.grounded is False
    assert generated.sources.count == 0

    # ---------------------------------------------------------
    # EMPTY QUERY
    # ---------------------------------------------------------

    print("\n")
    print("-" * 70)
    print("EMPTY QUERY")
    print("-" * 70)

    try:
        service.generate(
            query="   ",
            evidence=empty_evidence,
        )

        raise AssertionError(
            "Empty query should have raised ValueError."
        )

    except ValueError:
        print("Empty query correctly rejected.")

    print("\n")
    print("=" * 70)
    print("ANSWER GENERATION PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()