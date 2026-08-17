from pathlib import Path

from langchain_pymupdf4llm import PyMuPDF4LLMLoader

from ingestion.chunker import DocumentChunker
from ingestion.normalizer import DocumentNormalizer


PDF_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "knowledge_base"
    / "hr"
    / "remote_work_policy_v2.pdf"
)


def main():
    print("=" * 70)
    print("PDF CHUNKING")
    print("=" * 70)

    loader = PyMuPDF4LLMLoader(
        file_path=str(PDF_PATH),
        mode="page",
    )

    documents = loader.load()

    normalizer = DocumentNormalizer()
    chunker = DocumentChunker()

    for document in documents:
        normalized = normalizer.normalize(document)

        chunks = chunker.chunk(normalized)

        print(f"\nDocument: {normalized.title}")
        print(f"Document ID: {normalized.document_id}")
        print(f"Version: {normalized.version}")
        print(f"Chunks created: {len(chunks)}")

        for chunk in chunks:
            print("\n" + "-" * 70)

            print(
                f"Chunk ID: "
                f"{chunk.metadata['chunk_id']}"
            )

            print(
                f"Chunk index: "
                f"{chunk.metadata['chunk_index']}"
            )

            print(
                f"Total chunks: "
                f"{chunk.metadata['total_chunks']}"
            )

            print("\nContent:")
            print(chunk.page_content)


if __name__ == "__main__":
    main()