from evaluation.dataset import RETRIEVAL_TEST_CASES
from evaluation.evaluator import RetrievalEvaluator
from ingestion.models import KnowledgeDocument
from services.embedding_service import EmbeddingService
from services.retrieval_service import RetrievalService
from retrieval.vector_store import VectorStore
from ingestion.chunker import DocumentChunker


def build_retrieval_service() -> RetrievalService:
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
        content="""
# Remote Work Policy

Employees who have completed their probation period may request
remote work subject to manager approval.

International remote work requires prior approval from Human
Resources and the employee's manager.

The request must identify the destination country, expected duration,
and business justification.

International remote work may be approved for up to 90 consecutive
calendar days.

Requests exceeding 90 days require review by HR and the Compliance team.

Manager approval and HR approval are required before international
remote work begins.
""",
        content_hash="evaluation-demo",
    )

    chunker = DocumentChunker(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunks = chunker.chunk(document)

    embedding_service = EmbeddingService()

    embeddings = embedding_service.embed_documents(
        [chunk.page_content for chunk in chunks]
    )

    vector_store = VectorStore(
        dimension=embedding_service.dimension
    )

    vector_store.add(
        embeddings=embeddings,
        documents=chunks,
    )

    return RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        similarity_threshold=0.65,
    )


def main() -> None:
    print("=" * 70)
    print("RETRIEVAL EVALUATION")
    print("=" * 70)

    retrieval_service = build_retrieval_service()

    evaluator = RetrievalEvaluator(
        retrieval_service=retrieval_service
    )

    results = evaluator.evaluate(
        test_cases=RETRIEVAL_TEST_CASES,
        top_k=5,
    )

    print()
    print("-" * 70)

    hits = 0

    for index, result in enumerate(results, start=1):
        if result.hit:
            hits += 1

        print(f"Query {index}")
        print(f"Question: {result.query}")
        print(
            f"Expected: "
            f"{result.expected_document_id}"
        )
        print(
            f"Retrieved: "
            f"{result.retrieved_document_ids}"
        )
        print(f"Hit: {result.hit}")
        print(
            f"Reciprocal Rank: "
            f"{result.reciprocal_rank:.4f}"
        )
        print("-" * 70)

    total = len(results)

    hit_rate = (
        hits / total
        if total
        else 0.0
    )

    print()
    print("=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Queries evaluated: {total}")
    print(f"Successful cases: {hits}")
    print(f"Hit Rate: {hit_rate:.2%}")

    if hit_rate < 1.0:
        raise AssertionError(
            "Retrieval evaluation failed."
        )

    print()
    print("RETRIEVAL EVALUATION PASSED")


if __name__ == "__main__":
    main()