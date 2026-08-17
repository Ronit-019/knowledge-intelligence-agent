import os

from services.llm.base import LLMProvider
from services.llm.groq_provider import GroqProvider


def main():
    print("=" * 70)
    print("GROQ PROVIDER CONFIGURATION")
    print("=" * 70)

    # ---------------------------------------------------------
    # CONTRACT
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("PROVIDER CONTRACT")
    print("-" * 70)

    assert issubclass(
        GroqProvider,
        LLMProvider,
    )

    print("GroqProvider implements LLMProvider.")

    # ---------------------------------------------------------
    # MISSING API KEY
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("API KEY VALIDATION")
    print("-" * 70)

    original_key = os.environ.pop(
        "GROQ_API_KEY",
        None,
    )

    try:
        GroqProvider()

        raise AssertionError(
            "Provider should reject a missing GROQ_API_KEY."
        )

    except ValueError as exc:
        print(f"Correctly rejected missing API key: {exc}")

    finally:
        if original_key is not None:
            os.environ["GROQ_API_KEY"] = original_key

    # ---------------------------------------------------------
    # EMPTY PROMPT
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("PROMPT VALIDATION")
    print("-" * 70)

    if not os.getenv("GROQ_API_KEY"):
        print(
            "Skipping empty-prompt provider test because "
            "GROQ_API_KEY is not configured."
        )
    else:
        provider = GroqProvider()

        try:
            provider.generate("")

            raise AssertionError(
                "Empty prompt should have raised ValueError."
            )

        except ValueError:
            print("Empty prompt correctly rejected.")

    print("\n" + "=" * 70)
    print("GROQ PROVIDER CONFIGURATION TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()