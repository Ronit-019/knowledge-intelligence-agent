from pathlib import Path

from ingestion.normalizer import DocumentNormalizer
from services.ingestion_service import IngestionService


KNOWLEDGE_BASE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "knowledge_base"
)


def main():
    print("=" * 70)
    print("MULTI-DOCUMENT INGESTION")
    print("=" * 70)

    normalizer = DocumentNormalizer()

    ingestion_service = IngestionService(
        normalizer=normalizer
    )

    pdfs = ingestion_service.discover_pdfs(
        KNOWLEDGE_BASE
    )

    print(f"\nPDFs discovered: {len(pdfs)}")

    for pdf in pdfs:
        print(f"  - {pdf.relative_to(KNOWLEDGE_BASE)}")

    documents = ingestion_service.ingest(
        KNOWLEDGE_BASE
    )

    print("\n" + "-" * 70)
    print("NORMALIZED DOCUMENTS")
    print("-" * 70)

    for document in documents:
        print(
            f"\nDocument ID : {document.document_id}"
        )
        print(
            f"Title       : {document.title}"
        )
        print(
            f"Department  : {document.department}"
        )
        print(
            f"Type        : {document.document_type}"
        )
        print(
            f"Version     : {document.version}"
        )
        print(
            f"Effective   : {document.effective_date}"
        )
        print(
            f"Status      : {document.status}"
        )
        print(
            f"Supersedes  : {document.supersedes}"
        )
        print(
            f"Page        : {document.page}"
        )

    print("\n" + "=" * 70)
    print("MULTI-DOCUMENT INGESTION PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()