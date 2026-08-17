from services.llm.base import LLMProvider


class FakeLLMProvider(LLMProvider):
    """
    Fake provider used only for testing the interface.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:

        return f"FAKE RESPONSE: {prompt}"


def main():
    print("=" * 70)
    print("LLM PROVIDER INTERFACE")
    print("=" * 70)

    provider = FakeLLMProvider()

    response = provider.generate(
        "What is the remote work policy?"
    )

    print("\nProvider:", type(provider).__name__)
    print("Response:", response)

    assert response == (
        "FAKE RESPONSE: What is the remote work policy?"
    )

    # ---------------------------------------------------------
    # ABSTRACT CONTRACT VALIDATION
    # ---------------------------------------------------------

    print("\n" + "-" * 70)
    print("ABSTRACT CONTRACT VALIDATION")
    print("-" * 70)

    try:
        LLMProvider()

        raise AssertionError(
            "LLMProvider should not be directly instantiable."
        )

    except TypeError:
        print(
            "LLMProvider correctly rejected direct instantiation."
        )

    print("\n" + "=" * 70)
    print("LLM PROVIDER TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()