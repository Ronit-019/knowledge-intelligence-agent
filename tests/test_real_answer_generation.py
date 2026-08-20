from ingestion.models import KnowledgeDocument
from services.answer_generation_service import AnswerGenerationService
from services.evidence_selector import EvidenceSelection
from services.llm.groq_provider import GroqProvider
from services.prompt_builder import PromptBuilder
from services.retrieval_service import RetrievalResult


def main():
    print("=" * 70)
    print("REAL LLM ANSWER GENERATION")
    print("=" * 70)

    document = KnowledgeDocument(
        document_id="HR-RW-001",
        title="Remote Work Policy",
        department="HR",
        document_type="policy",
        version="2.0",
        effective_date="2026-01-01",
        status="active",
        source="internal-policy-demo",
        supersedes="HR-RW-001:v1.0",
        page=1,
        content=(
            "International remote work requires prior approval "
            "from Human Resources and the employee's manager. "
            "International remote work may be approved for up "
            "to 90 consecutive calendar days."
        ),
        content_hash="test-hash",
    )

    from langchain_core.documents import Document

    chunk = Document(
        page_content=document.content,
        metadata={
            "document_id": document.document_id,
            "title": document.title,
            "department": document.department,
            "document_type": document.document_type,
            "version": document.version,
            "effective_date": document.effective_date,
            "status": document.status,
            "source": document.source,
            "supersedes": document.supersedes,
            "page": document.page,
            "chunk_id": "HR-RW-001:2.0:1:0",
        },
    )

    retrieval_result = RetrievalResult(
        document=chunk,
        semantic_score=0.95,
    )

    evidence = EvidenceSelection(
        results=[retrieval_result]
    )

    provider = GroqProvider(
        model_name="openai/gpt-oss-20b"
    )

    prompt_builder = PromptBuilder()

    service = AnswerGenerationService(
        llm_provider=provider,
        prompt_builder=prompt_builder,
    )

    query = "How long can an employee work from another country?"

    result = service.generate(
        query=query,
        evidence=evidence,
    )

    print()
    print("-" * 70)
    print("QUESTION")
    print("-" * 70)
    print(query)

    print()
    print("-" * 70)
    print("GENERATED ANSWER")
    print("-" * 70)
    print(result.answer)

    print()
    print("-" * 70)
    print("VALIDATION")
    print("-" * 70)

    print(f"Grounded: {result.grounded}")
    print(f"Sources: {result.sources.count}")

    assert result.grounded is True
    assert result.sources.count == 1
    assert result.answer.strip()

    print()
    print("=" * 70)
    print("REAL LLM ANSWER GENERATION PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()