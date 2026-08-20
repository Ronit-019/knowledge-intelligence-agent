from langchain_core.documents import Document

from services.evidence_selector import EvidenceSelection
from services.retrieval_service import RetrievalResult
from services.prompt_builder import PromptBuilder


def main():
    print("=" * 70)
    print("PROMPT BUILDER")
    print("=" * 70)

    document = Document(
        page_content=(
            "International remote work may be approved "
            "for up to 90 consecutive calendar days."
        ),
        metadata={
            "document_id": "HR-RW-001",
            "title": "Remote Work Policy",
            "version": "2.0",
            "page": 1,
            "chunk_id": "HR-RW-001:2.0:1:0",
        },
    )

    result = RetrievalResult(
        document=document,
        semantic_score=0.7347,
    )

    evidence = EvidenceSelection(
        results=[result]
    )

    builder = PromptBuilder()

    query = (
        "How long can an employee work "
        "from another country?"
    )

    prompt = builder.build(
        query=query,
        evidence=evidence,
    )

    print()
    print("-" * 70)
    print("GENERATED PROMPT")
    print("-" * 70)
    print(prompt)

    assert query in prompt
    assert "90 consecutive calendar days" in prompt
    assert "HR-RW-001" in prompt
    assert "Remote Work Policy" in prompt
    assert "2.0" in prompt
    assert "Do not use outside knowledge." in prompt
    assert "Do not invent or assume information." in prompt

    print()
    print("-" * 70)
    print("EMPTY QUERY VALIDATION")
    print("-" * 70)

    try:
        builder.build(
            query="   ",
            evidence=evidence,
        )
    except ValueError:
        print("Empty query correctly rejected.")
    else:
        raise AssertionError(
            "Empty query was not rejected."
        )

    print()
    print("-" * 70)
    print("EMPTY EVIDENCE VALIDATION")
    print("-" * 70)

    empty_evidence = EvidenceSelection(
        results=[]
    )

    try:
        builder.build(
            query=query,
            evidence=empty_evidence,
        )
    except ValueError:
        print("Empty evidence correctly rejected.")
    else:
        raise AssertionError(
            "Empty evidence was not rejected."
        )

    print()
    print("=" * 70)
    print("PROMPT BUILDER TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()