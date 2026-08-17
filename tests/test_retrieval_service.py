from ingestion.models import KnowledgeDocument
from ingestion.chunker import DocumentChunker
from services.embedding_service import EmbeddingService
from services.retrieval_service import RetrievalService
from retrieval.vector_store import VectorStore


def main():
    print("=" * 70)
    print("RETRIEVAL SERVICE")
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

Requests exceeding 90 days require review by HR and the Compliance
team.

Manager approval and HR approval are required before international
remote work begins.
""",
        content_hash="test-hash",
    )

    # --------------------------------------------------------------
    # CHUNK
    # --------------------------------------------------------------

    chunker = DocumentChunker()

    chunks = chunker.chunk(document)

    print(f"\nChunks created: {len(chunks)}")

    # --------------------------------------------------------------
    # EMBEDDING
    # --------------------------------------------------------------

    embedding_service = EmbeddingService()

    embeddings = embedding_service.embed_documents(
        [
            chunk.page_content
            for chunk in chunks
        ]
    )

    # --------------------------------------------------------------
    # VECTOR STORE
    # --------------------------------------------------------------

    vector_store = VectorStore(
        dimension=embedding_service.dimension
    )

    vector_store.add(
        embeddings=embeddings,
        documents=chunks,
    )

    print(
        f"Indexed documents: {vector_store.size}"
    )

    # --------------------------------------------------------------
    # RETRIEVAL SERVICE
    # --------------------------------------------------------------

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        similarity_threshold=0.65,
    )

    # --------------------------------------------------------------
    # SUPPORTED QUERY
    # --------------------------------------------------------------

    query = (
        "How long can an employee work from another country?"
    )

    results = retrieval_service.search(
        query=query,
        top_k=3,
    )

    print("\n" + "-" * 70)
    print("SUPPORTED QUERY")
    print("-" * 70)
    print(query)

    print(
        f"\nEvidence returned: {len(results)}"
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print(f"\nRank: {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Chunk: {result.chunk_id}")
        print(f"Document: {result.title}")
        print(f"Version: {result.version}")
        print(f"Page: {result.page}")

    # --------------------------------------------------------------
    # UNSUPPORTED QUERY
    # --------------------------------------------------------------

    unsupported_query = (
        "What is the company's maternity leave policy?"
    )

    unsupported_results = retrieval_service.search(
        query=unsupported_query,
        top_k=3,
    )

    print("\n" + "-" * 70)
    print("UNSUPPORTED QUERY")
    print("-" * 70)
    print(unsupported_query)

    print(
        f"\nEvidence returned: "
        f"{len(unsupported_results)}"
    )

    for rank, result in enumerate(
        unsupported_results,
        start=1,
    ):
        print(f"\nRank: {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Chunk: {result.chunk_id}")
        print(f"Document: {result.title}")

    if unsupported_results:
        raise AssertionError(
            "Unsupported query incorrectly returned evidence."
        )

    # --------------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------------

    if not results:
        raise AssertionError(
            "Expected relevant evidence."
        )

    print("\n" + "=" * 70)
    print("RETRIEVAL SERVICE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()