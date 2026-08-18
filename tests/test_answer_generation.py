from services.answer_generation_service import AnswerGenerationService
from services.evidence_selector import EvidenceSelection
from services.prompt_builder import PromptBuilder
from services.llm.base import LLMProvider


class FakeLLMProvider(LLMProvider):
    def generate(self, prompt: str) -> str:
        return "International remote work may be approved for up to 90 consecutive calendar days."


def main():

    print("=" * 70)
    print("ANSWER GENERATION")
    print("=" * 70)

    llm_provider = FakeLLMProvider()
    prompt_builder = PromptBuilder()

    service = AnswerGenerationService(
        llm_provider=llm_provider,
        prompt_builder=prompt_builder,
    )

    # ---------------------------------------------------------
    # SUPPORTED QUERY
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("SUPPORTED QUERY")
    print("-" * 70)

    evidence = EvidenceSelection(
        results=[
            # Keep your existing RetrievalResult here
        ]
    )

    result = service.generate(
        query="How long can an employee work from another country?",
        evidence=evidence,
    )

    print("\nAnswer:")
    print(result.answer)

    assert result.grounded is True
    assert result.sources.count > 0

    # ---------------------------------------------------------
    # UNSUPPORTED QUERY
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("UNSUPPORTED QUERY")
    print("-" * 70)

    empty_evidence = EvidenceSelection(
        results=[]
    )

    result = service.generate(
        query="What is the company's dental insurance policy?",
        evidence=empty_evidence,
    )

    print("\nAnswer:")
    print(result.answer)

    assert result.grounded is False
    assert result.sources.count == 0

    # ---------------------------------------------------------
    # EMPTY QUERY
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("EMPTY QUERY")
    print("-" * 70)

    try:
        service.generate(
            query="",
            evidence=evidence,
        )

        raise AssertionError(
            "Empty query should have been rejected."
        )

    except ValueError:
        print("Empty query correctly rejected.")

    print("\n" + "=" * 70)
    print("ANSWER GENERATION TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()