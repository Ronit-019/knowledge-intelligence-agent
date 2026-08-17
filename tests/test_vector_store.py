from ingestion.models import KnowledgeDocument
from ingestion.chunker import DocumentChunker
from services.embedding_service import EmbeddingService
from retrieval.vector_store import VectorStore


def main():
    print("=" * 70)
    print("VECTOR STORE + SEMANTIC RETRIEVAL")
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
    # EMBEDDINGS
    # --------------------------------------------------------------

    embedding_service = EmbeddingService()

    embeddings = embedding_service.embed_documents(
        [
            chunk.page_content
            for chunk in chunks
        ]
    )

    print(
        f"Embedding dimension: "
        f"{embedding_service.dimension}"
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
    # QUERY
    # --------------------------------------------------------------

    query = (
        "How long can an employee work from another country?"
    )

    query_embedding = embedding_service.embed_text(
        query
    )

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=3,
    )

    print("\n" + "-" * 70)
    print("QUERY")
    print("-" * 70)
    print(query)

    print("\n" + "-" * 70)
    print("RETRIEVED RESULTS")
    print("-" * 70)

    for rank, (document, score) in enumerate(
        results,
        start=1,
    ):
        print(f"\nRank: {rank}")
        print(
            f"Score: {score:.4f}"
        )
        print(
            f"Chunk ID: "
            f"{document.metadata['chunk_id']}"
        )
        print(
            f"Document: "
            f"{document.metadata['title']}"
        )
        print(
            f"Version: "
            f"{document.metadata['version']}"
        )
        print("\nContent:")
        print(document.page_content)

    print("\n" + "=" * 70)
    print("VECTOR RETRIEVAL TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()