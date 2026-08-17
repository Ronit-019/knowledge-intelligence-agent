from pathlib import Path

from ingestion.chunker import DocumentChunker
from ingestion.normalizer import DocumentNormalizer
from services.chunking_service import ChunkingService
from services.ingestion_service import IngestionService


KNOWLEDGE_BASE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "knowledge_base"
)


def main():
    print("=" * 70)
    print("MULTI-DOCUMENT CHUNKING")
    print("=" * 70)

    normalizer = DocumentNormalizer()

    ingestion_service = IngestionService(
        normalizer=normalizer
    )

    documents = ingestion_service.ingest(
        KNOWLEDGE_BASE
    )

    print(
        f"\nNormalized documents: {len(documents)}"
    )

    chunker = DocumentChunker(
        chunk_size=1000,
        chunk_overlap=150,
    )

    chunking_service = ChunkingService(
        chunker=chunker
    )

    chunks = chunking_service.chunk_documents(
        documents
    )

    print(
        f"Total chunks created: {len(chunks)}"
    )

    print("\n" + "-" * 70)
    print("CHUNK DISTRIBUTION")
    print("-" * 70)

    document_counts: dict[str, int] = {}

    for chunk in chunks:
        document_id = chunk.metadata[
            "document_id"
        ]

        document_counts[document_id] = (
            document_counts.get(document_id, 0) + 1
        )

    for document_id, count in document_counts.items():
        print(
            f"{document_id}: {count} chunks"
        )

    print("\n" + "-" * 70)
    print("SAMPLE CHUNKS")
    print("-" * 70)

    for chunk in chunks[:5]:
        print(
            f"\nChunk ID : "
            f"{chunk.metadata['chunk_id']}"
        )

        print(
            f"Document : "
            f"{chunk.metadata['title']}"
        )

        print(
            f"Version  : "
            f"{chunk.metadata['version']}"
        )

        print(
            f"Department : "
            f"{chunk.metadata['department']}"
        )

        print(
            f"Content:\n{chunk.page_content[:500]}"
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    assert chunks, (
        "Chunking produced no chunks."
    )

    for chunk in chunks:
        assert "document_id" in chunk.metadata
        assert "chunk_id" in chunk.metadata
        assert "chunk_index" in chunk.metadata
        assert "total_chunks" in chunk.metadata
        assert "version" in chunk.metadata

    # Ensure both versions survived chunking.
    remote_work_versions = {
        chunk.metadata["version"]
        for chunk in chunks
        if chunk.metadata["document_id"]
        == "HR-RW-001"
    }

    assert "1.0" in remote_work_versions
    assert "2.0" in remote_work_versions

    print("\n" + "=" * 70)
    print("MULTI-DOCUMENT CHUNKING PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()