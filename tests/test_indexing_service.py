from pathlib import Path

from langchain_pymupdf4llm import PyMuPDF4LLMLoader

from ingestion.chunker import DocumentChunker
from ingestion.normalizer import DocumentNormalizer
from retrieval.vector_store import VectorStore
from services.embedding_service import EmbeddingService
from services.indexing_service import IndexingService


KNOWLEDGE_BASE = Path(
    "data/knowledge_base"
)


def load_documents():
    """
    Load and normalize every PDF in the knowledge base.
    """

    loader_results = []

    normalizer = DocumentNormalizer()

    pdf_files = sorted(
        KNOWLEDGE_BASE.rglob("*.pdf")
    )

    for pdf_path in pdf_files:

        loader = PyMuPDF4LLMLoader(
            str(pdf_path)
        )

        documents = loader.load()

        for document in documents:
            normalized = normalizer.normalize(
                document
            )

            loader_results.append(
                normalized
            )

    return loader_results


def main():

    print("=" * 70)
    print("MULTI-DOCUMENT INDEXING")
    print("=" * 70)

    normalized_documents = load_documents()

    assert normalized_documents

    print(
        f"\nNormalized documents: "
        f"{len(normalized_documents)}"
    )

    chunker = DocumentChunker()

    chunks = []

    for document in normalized_documents:

        document_chunks = chunker.chunk(
            document
        )

        chunks.extend(
            document_chunks
        )

    assert chunks

    print(
        f"Total chunks: {len(chunks)}"
    )

    embedding_service = EmbeddingService()

    vector_store = VectorStore(
        dimension=embedding_service.dimension
    )

    indexing_service = IndexingService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    result = indexing_service.index(
        chunks
    )

    print("\n" + "-" * 70)
    print("INDEXING RESULT")
    print("-" * 70)

    print(
        f"Documents indexed: "
        f"{result.documents_indexed}"
    )

    print(
        f"Embedding dimension: "
        f"{result.embedding_dimension}"
    )

    print(
        f"Vector store size: "
        f"{vector_store.size}"
    )

    # --------------------------------------------------------------
    # CONTRACT CHECKS
    # --------------------------------------------------------------

    assert result.documents_indexed == len(chunks)

    assert vector_store.size == len(chunks)

    assert (
        result.embedding_dimension
        == embedding_service.dimension
    )

    assert (
        vector_store.dimension
        == embedding_service.dimension
    )

    print("\nIndex count: OK")
    print("Embedding dimension: OK")
    print("Vector store size: OK")

    print("\n" + "=" * 70)
    print("MULTI-DOCUMENT INDEXING PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()