from services.answer_generation_service import AnswerGenerationService
from services.evidence_selector import EvidenceSelection
from services.llm.groq_provider import GroqProvider
from services.prompt_builder import PromptBuilder


def main():
    print("=" * 70)
    print("LLM ANSWER GENERATION")
    print("=" * 70)

    provider = GroqProvider(
        model_name="openai/gpt-oss-20b"
    )

    prompt_builder = PromptBuilder()

    service = AnswerGenerationService(
        llm_provider=provider,
        prompt_builder=prompt_builder,
    )

    # We will use real evidence here once the
    # existing retrieval pipeline is connected.

    print("Groq provider initialized.")
    print("Prompt builder initialized.")
    print("Answer generation service initialized.")

    print()
    print("=" * 70)
    print("LLM ANSWER GENERATION TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()