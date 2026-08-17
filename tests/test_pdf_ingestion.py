from pathlib import Path

from langchain_pymupdf4llm import PyMuPDF4LLMLoader

from ingestion.normalizer import DocumentNormalizer


ROOT = Path(__file__).resolve().parents[1]

PDF_PATH = (
    ROOT
    / "data"
    / "knowledge_base"
    / "hr"
    / "remote_work_policy_v2.pdf"
)


def main():
    loader = PyMuPDF4LLMLoader(
        file_path=str(PDF_PATH),
        mode="page",
    )

    documents = loader.load()

    normalizer = DocumentNormalizer()

    print("=" * 70)
    print("PDF INGESTION + NORMALIZATION")
    print("=" * 70)

    print(f"PDF: {PDF_PATH.name}")
    print(f"Pages returned: {len(documents)}")

    for document in documents:
        normalized = normalizer.normalize(document)

        print("\n" + "-" * 70)

        print("Document ID:", normalized.document_id)
        print("Title:", normalized.title)
        print("Department:", normalized.department)
        print("Type:", normalized.document_type)
        print("Version:", normalized.version)
        print("Effective:", normalized.effective_date)
        print("Status:", normalized.status)
        print("Supersedes:", normalized.supersedes)
        print("Page:", normalized.page)
        print("Hash:", normalized.content_hash)
        print("Content length:", len(normalized.content))

        print("\nContent preview:")
        print(normalized.content[:500])


if __name__ == "__main__":
    main()