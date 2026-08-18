from pathlib import Path

from registry.document_registry import DocumentRegistry
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.ingestion_service import IngestionService
from services.knowledge_base_service import KnowledgeBaseService
from services.retrieval_service import RetrievalService
from ingestion.chunker import DocumentChunker
from ingestion.normalizer import DocumentNormalizer


def main():
    print("=" * 70)
    print("ACTIVE VERSION RETRIEVAL")
    print("=" * 70)

    # ---------------------------------------------------------
    # Build the knowledge base through the real pipeline.
    # ---------------------------------------------------------

    normalizer = DocumentNormalizer()

    ingestion_service = IngestionService(
        normalizer=normalizer,
    )

    registry = DocumentRegistry()

    chunking_service = ChunkingService(
        chunker=DocumentChunker(),
    )

    embedding_service = EmbeddingService()

    knowledge_base_service = KnowledgeBaseService(
        ingestion_service=ingestion_service,
        document_registry=registry,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
    )

    knowledge_base = knowledge_base_service.build(
        Path("data/knowledge_base")
    )

    # ---------------------------------------------------------
    # Create retrieval service over the active-only index.
    # ---------------------------------------------------------

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=knowledge_base.vector_store,
        similarity_threshold=0.60,
    )

    query = (
        "How long can an employee work from another country?"
    )

    print()
    print("-" * 70)
    print("QUERY")
    print("-" * 70)
    print(query)

    results = retrieval_service.search(
        query=query,
        top_k=10,
    )

    print()
    print("-" * 70)
    print("RETRIEVED EVIDENCE")
    print("-" * 70)

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print()
        print(f"Rank: {rank}")
        print(f"Score: {result.score:.4f}")
        print(f"Document: {result.document_id}")
        print(f"Version: {result.version}")
        print(f"Status: {result.document.metadata.get('status')}")
        print(f"Chunk: {result.chunk_id}")

    # ---------------------------------------------------------
    # Critical invariant:
    # No inactive document may ever be retrieved.
    # ---------------------------------------------------------

    print()
    print("-" * 70)
    print("ACTIVE VERSION VALIDATION")
    print("-" * 70)

    for result in results:
        assert registry.is_active(
            result.document_id,
            result.version,
        ), (
            "Inactive document retrieved: "
            f"{result.document_id}:{result.version}"
        )

    print(
        "All retrieved evidence belongs to active "
        "document versions."
    )

    # ---------------------------------------------------------
    # Specific stale-version protection.
    # ---------------------------------------------------------

    hr_remote_results = [
        result
        for result in results
        if result.document_id == "HR-RW-001"
    ]

    hr_remote_versions = {
        result.version
        for result in hr_remote_results
    }

    print()
    print(
        "HR-RW-001 retrieved versions:",
        sorted(hr_remote_versions),
    )

    assert "1.0" not in hr_remote_versions, (
        "Superseded HR-RW-001 v1.0 was retrieved."
    )

    if hr_remote_results:
        assert hr_remote_versions == {"2.0"}, (
            "Unexpected HR-RW-001 version retrieved."
        )

    print(
        "Superseded HR-RW-001 v1.0 was not retrieved."
    )

    # ---------------------------------------------------------
    # Final validation.
    # ---------------------------------------------------------

    assert results, (
        "Expected relevant evidence but retrieved nothing."
    )

    print()
    print("=" * 70)
    print("ACTIVE VERSION RETRIEVAL PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()