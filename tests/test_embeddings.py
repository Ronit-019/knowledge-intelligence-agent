from ingestion.models import KnowledgeDocument
from ingestion.chunker import DocumentChunker
from services.embedding_service import EmbeddingService


def main():
    print("=" * 70)
    print("DOCUMENT EMBEDDING")
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
# **Remote Work Policy**

**Document ID:** HR-RW-001
**Department:** HR
**Document Type:** policy
**Version:** 2.0
**Effective Date:** 2026-01-01

**Status:** active
**Source:** internal-policy-demo

## **Purpose**

This policy defines the current requirements for remote and hybrid
work arrangements.

## **Remote Work Eligibility**

Employees who have completed their probation period may request
remote work subject to manager approval.

## **International Remote Work**

International remote work requires prior approval from Human
Resources and the employee's manager.

## **Duration**

International remote work may be approved for up to 90 consecutive
calendar days.

## **Manager Approval**

Manager approval and HR approval are required before international
remote work begins.
""",
        content_hash="test-hash",
    )

    # --------------------------------------------------------------
    # CHUNKING
    # --------------------------------------------------------------

    chunker = DocumentChunker()
    chunks = chunker.chunk(document)

    print(f"\nChunks created: {len(chunks)}")

    # --------------------------------------------------------------
    # EMBEDDING
    # --------------------------------------------------------------

    embedding_service = EmbeddingService()

    print(f"Model: {embedding_service.model_name}")
    print(f"Embedding dimension: {embedding_service.dimension}")

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    embeddings = embedding_service.embed_documents(texts)

    # --------------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------------

    print("\n" + "-" * 70)
    print("EMBEDDING VALIDATION")
    print("-" * 70)

    assert len(embeddings) == len(chunks), (
        "Number of embeddings does not match number of chunks."
    )

    for chunk, embedding in zip(chunks, embeddings):

        chunk_id = chunk.metadata["chunk_id"]

        assert len(embedding) == embedding_service.dimension, (
            f"Invalid embedding dimension for {chunk_id}"
        )

        print(f"\nChunk ID: {chunk_id}")
        print(f"Chunk index: {chunk.metadata['chunk_index']}")
        print(f"Vector dimensions: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")

    print("\n" + "=" * 70)
    print("EMBEDDING TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()