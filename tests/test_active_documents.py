from services.ingestion_service import IngestionService
from ingestion.normalizer import DocumentNormalizer
from registry.document_registry import DocumentRegistry


def main():
    print("=" * 70)
    print("ACTIVE DOCUMENT RESOLUTION")
    print("=" * 70)

    # ---------------------------------------------------------
    # INGEST REAL KNOWLEDGE BASE
    # ---------------------------------------------------------

    ingestion_service = IngestionService(
        normalizer=DocumentNormalizer(),
    )

    documents = ingestion_service.ingest(
        "data/knowledge_base"
    )

    # ---------------------------------------------------------
    # BUILD REGISTRY
    # ---------------------------------------------------------

    registry = DocumentRegistry()

    registry.register_many(documents)

    print(
        f"\nDocument versions registered: {registry.size}"
    )

    # ---------------------------------------------------------
    # RESOLVE ACTIVE DOCUMENTS
    # ---------------------------------------------------------

    active_documents = registry.get_active_documents()

    print(
        f"Active document versions: {len(active_documents)}"
    )

    print("\nACTIVE DOCUMENTS")
    print("-" * 70)

    for document in sorted(
        active_documents,
        key=lambda item: item.document_id,
    ):
        print(
            f"{document.document_id} | "
            f"v{document.version} | "
            f"{document.status}"
        )

    # ---------------------------------------------------------
    # VALIDATE
    # ---------------------------------------------------------

    expected_active = {
        ("CMP-DH-005", "1.0"),
        ("FIN-EXP-003", "1.0"),
        ("HR-IW-002", "1.0"),
        ("HR-RW-001", "2.0"),
        ("SEC-ACC-004", "2.0"),
    }

    actual_active = {
        (
            document.document_id,
            document.version,
        )
        for document in active_documents
    }

    assert actual_active == expected_active

    # ---------------------------------------------------------
    # MAKE SURE SUPERSEDED VERSION IS EXCLUDED
    # ---------------------------------------------------------

    assert (
        "HR-RW-001",
        "1.0",
    ) not in actual_active

    print(
        "\nSuperseded HR-RW-001 v1.0 correctly excluded."
    )

    print("\n" + "=" * 70)
    print("ACTIVE DOCUMENT RESOLUTION PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()