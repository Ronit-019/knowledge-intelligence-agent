from ingestion.models import KnowledgeDocument
from registry.document_registry import DocumentRegistry


def make_document(
    document_id: str,
    version: str,
    status: str,
    supersedes: str | None = None,
) -> KnowledgeDocument:
    return KnowledgeDocument(
        document_id=document_id,
        title="Remote Work Policy",
        department="HR",
        document_type="policy",
        version=version,
        effective_date="2026-01-01",
        status=status,
        source="internal-policy-demo",
        supersedes=supersedes,
        page=1,
        content="Test document content.",
        content_hash=f"hash-{version}",
    )


def main():
    print("=" * 70)
    print("DOCUMENT REGISTRY")
    print("=" * 70)

    registry = DocumentRegistry()

    v1 = make_document(
        document_id="HR-RW-001",
        version="1.0",
        status="superseded",
    )

    v2 = make_document(
        document_id="HR-RW-001",
        version="2.0",
        status="active",
        supersedes="HR-RW-001:v1.0",
    )

    # ---------------------------------------------------------
    # REGISTER
    # ---------------------------------------------------------

    registry.register(v1)
    registry.register(v2)

    assert registry.size == 2

    print("\nRegistered versions:", registry.size)

    # ---------------------------------------------------------
    # GET ALL VERSIONS
    # ---------------------------------------------------------

    versions = registry.get_versions("HR-RW-001")

    assert len(versions) == 2
    assert {doc.version for doc in versions} == {
        "1.0",
        "2.0",
    }

    print("Versions:", [doc.version for doc in versions])

    # ---------------------------------------------------------
    # ACTIVE VERSION
    # ---------------------------------------------------------

    active = registry.get_active("HR-RW-001")

    assert active is not None
    assert active.version == "2.0"
    assert active.status == "active"

    print("Active version:", active.version)

    # ---------------------------------------------------------
    # IS ACTIVE
    # ---------------------------------------------------------

    assert registry.is_active(
        "HR-RW-001",
        "1.0",
    ) is False

    assert registry.is_active(
        "HR-RW-001",
        "2.0",
    ) is True

    print("v1.0 active:", registry.is_active("HR-RW-001", "1.0"))
    print("v2.0 active:", registry.is_active("HR-RW-001", "2.0"))

    # ---------------------------------------------------------
    # UNKNOWN DOCUMENT
    # ---------------------------------------------------------

    assert registry.get_active(
        "UNKNOWN-001"
    ) is None

    assert registry.get_versions(
        "UNKNOWN-001"
    ) == []

    assert registry.is_active(
        "UNKNOWN-001",
        "1.0",
    ) is False

    print("Unknown document handling: OK")

    # ---------------------------------------------------------
    # DUPLICATE VERSION
    # ---------------------------------------------------------

    try:
        registry.register(v2)
    except ValueError:
        print("Duplicate version correctly rejected.")
    else:
        raise AssertionError(
            "Duplicate document version was not rejected."
        )

    # ---------------------------------------------------------
    # MULTIPLE ACTIVE VERSIONS
    # ---------------------------------------------------------

    broken_registry = DocumentRegistry()

    active_v1 = make_document(
        document_id="BROKEN-001",
        version="1.0",
        status="active",
    )

    active_v2 = make_document(
        document_id="BROKEN-001",
        version="2.0",
        status="active",
    )

    broken_registry.register(active_v1)
    broken_registry.register(active_v2)

    try:
        broken_registry.get_active("BROKEN-001")
    except ValueError:
        print("Multiple active versions correctly rejected.")
    else:
        raise AssertionError(
            "Multiple active versions were not detected."
        )

    # ---------------------------------------------------------
    # ACTIVE DOCUMENT COLLECTION
    # ---------------------------------------------------------

    active_documents = registry.get_active_documents()

    assert len(active_documents) == 1

    assert active_documents[0].document_id == "HR-RW-001"
    assert active_documents[0].version == "2.0"
    assert active_documents[0].status == "active"

    print(
        "Active document collection: OK"
    )
    
    print("\n" + "=" * 70)
    print("DOCUMENT REGISTRY TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()