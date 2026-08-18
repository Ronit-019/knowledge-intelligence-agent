from pathlib import Path

from registry.document_registry import DocumentRegistry
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.ingestion_service import IngestionService
from services.knowledge_base_service import KnowledgeBaseService
from ingestion.chunker import DocumentChunker
from ingestion.normalizer import DocumentNormalizer


def main():
    print("=" * 70)
    print("KNOWLEDGE BASE SERVICE")
    print("=" * 70)

    knowledge_base_path = Path("data/knowledge_base")

    normalizer = DocumentNormalizer()

    ingestion_service = IngestionService(
        normalizer=normalizer,
    )

    registry = DocumentRegistry()

    chunker = DocumentChunker()

    chunking_service = ChunkingService(
        chunker=chunker,
    )

    embedding_service = EmbeddingService()

    service = KnowledgeBaseService(
        ingestion_service=ingestion_service,
        document_registry=registry,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
    )

    knowledge_base = service.build(
        knowledge_base_path
    )

    print()
    print("-" * 70)
    print("KNOWLEDGE BASE RESULT")
    print("-" * 70)

    print(
        f"Registered versions: {registry.size}"
    )

    print(
        f"Active documents: "
        f"{len(knowledge_base.documents)}"
    )

    print(
        f"Active chunks: "
        f"{len(knowledge_base.chunks)}"
    )

    print(
        f"Indexed documents: "
        f"{knowledge_base.indexed_documents}"
    )

    print(
        f"Embedding dimension: "
        f"{knowledge_base.embedding_dimension}"
    )

    print()
    print("-" * 70)
    print("ACTIVE DOCUMENTS")
    print("-" * 70)

    for document in knowledge_base.documents:
        print(
            f"{document.document_id} | "
            f"v{document.version} | "
            f"{document.status}"
        )

    # ---------------------------------------------------------
    # Critical invariant:
    # Superseded HR-RW-001 v1.0 must NEVER reach the index.
    # ---------------------------------------------------------

    indexed_hr_versions = {
        document.metadata["version"]
        for document in knowledge_base.vector_store.documents
        if document.metadata["document_id"] == "HR-RW-001"
    }

    print()
    print("-" * 70)
    print("ACTIVE VERSION INDEX VALIDATION")
    print("-" * 70)

    print(
        "Indexed HR-RW-001 versions:",
        sorted(indexed_hr_versions),
    )

    assert indexed_hr_versions == {"2.0"}, (
        "Superseded HR-RW-001 v1.0 was indexed."
    )

    # ---------------------------------------------------------
    # Verify every indexed document is active.
    # ---------------------------------------------------------

    for document in knowledge_base.vector_store.documents:
        document_id = document.metadata["document_id"]
        version = document.metadata["version"]

        assert registry.is_active(
            document_id,
            version,
        ), (
            f"Inactive document indexed: "
            f"{document_id}:{version}"
        )

    print()
    print(
        "All indexed chunks belong to active document versions."
    )

    print()
    print("=" * 70)
    print("KNOWLEDGE BASE SERVICE PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()