from services.ingestion_service import IngestionService
from ingestion.normalizer import DocumentNormalizer
from registry.document_registry import DocumentRegistry

def main():
    print("=" * 70)
    print("REGISTRY + REAL DOCUMENT INGESTION")
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

    print(f"\nDocuments ingested: {len(documents)}")

    # ---------------------------------------------------------
    # REGISTER DOCUMENTS
    # ---------------------------------------------------------

    registry = DocumentRegistry()

    registry.register_many(documents)

    print(
        f"Document versions registered: {registry.size}"
    )

    # ---------------------------------------------------------
    # REMOTE WORK POLICY
    # ---------------------------------------------------------

    versions = registry.get_versions(
        "HR-RW-001"
    )

    print("\nHR-RW-001 VERSIONS")

    for document in versions:
        print(
            f"Version: {document.version} | "
            f"Status: {document.status} | "
            f"Effective: {document.effective_date}"
        )

    assert len(versions) == 2

    # ---------------------------------------------------------
    # ACTIVE VERSION
    # ---------------------------------------------------------

    active = registry.get_active(
        "HR-RW-001"
    )

    assert active is not None
    assert active.version == "2.0"
    assert active.status == "active"

    print(
        f"\nActive version: {active.version}"
    )

    # ---------------------------------------------------------
    # SUPSERSEDED VERSION
    # ---------------------------------------------------------

    assert registry.is_active(
        "HR-RW-001",
        "1.0",
    ) is False

    assert registry.is_active(
        "HR-RW-001",
        "2.0",
    ) is True

    print("Superseded version correctly identified.")

    # ---------------------------------------------------------
    # OTHER DOCUMENTS
    # ---------------------------------------------------------

    expected_documents = {
        "CMP-DH-005",
        "FIN-EXP-003",
        "HR-IW-002",
        "HR-RW-001",
        "SEC-ACC-004",
    }

    registered_documents = {
        document.document_id
        for document in documents
    }

    assert registered_documents == expected_documents

    print(
        "\nRegistered document IDs:"
    )

    for document_id in sorted(
        registered_documents
    ):
        print(f"  - {document_id}")

    # ---------------------------------------------------------
    # FINAL VALIDATION
    # ---------------------------------------------------------

    assert registry.size == len(documents)

    print(
        f"\nTotal registered versions: {registry.size}"
    )

    print("\n" + "=" * 70)
    print("REGISTRY + REAL INGESTION TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()