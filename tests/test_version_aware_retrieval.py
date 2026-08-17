from pathlib import Path

from langchain_pymupdf4llm import PyMuPDF4LLMLoader

from ingestion.normalizer import DocumentNormalizer
from ingestion.chunker import DocumentChunker
from services.embedding_service import EmbeddingService
from services.indexing_service import IndexingService
from services.retrieval_service import RetrievalService
from retrieval.vector_store import VectorStore


KNOWLEDGE_BASE = Path(
    "data/knowledge_base"
)


def build_retrieval_service():

    normalizer = DocumentNormalizer()
    chunker = DocumentChunker()

    normalized_documents = []

    for pdf_path in sorted(
        KNOWLEDGE_BASE.rglob("*.pdf")
    ):
        loader = PyMuPDF4LLMLoader(
            str(pdf_path)
        )

        documents = loader.load()

        for document in documents:
            normalized_documents.append(
                normalizer.normalize(document)
            )

    chunks = []

    for document in normalized_documents:
        chunks.extend(
            chunker.chunk(document)
        )

    embedding_service = EmbeddingService()

    vector_store = VectorStore(
        dimension=embedding_service.dimension
    )

    indexing_service = IndexingService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    indexing_service.index(chunks)

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        similarity_threshold=0.65,
    )

    return retrieval_service


def main():

    print("=" * 70)
    print("VERSION-AWARE RETRIEVAL")
    print("=" * 70)

    retrieval_service = build_retrieval_service()

    query = (
        "How long can an employee work "
        "from another country?"
    )

    print("\n" + "-" * 70)
    print("QUERY")
    print("-" * 70)
    print(query)

    results = retrieval_service.search(
        query=query,
        top_k=5,
    )

    print("\n" + "-" * 70)
    print("ACTIVE EVIDENCE")
    print("-" * 70)

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\nRank: {rank}"
        )
        print(
            f"Score: {result.score:.4f}"
        )
        print(
            f"Document: {result.document_id}"
        )
        print(
            f"Version: {result.version}"
        )
        print(
            f"Status: {result.status}"
        )
        print(
            f"Chunk: {result.chunk_id}"
        )

    assert results, (
        "Expected evidence but retrieved nothing."
    )

    for result in results:
        assert result.status.lower() != "superseded", (
            "Superseded document was returned."
        )

    assert any(
        result.document_id == "HR-RW-001"
        and result.version == "2.0"
        for result in results
    ), (
        "Active HR-RW-001 version 2.0 "
        "was not retrieved."
    )

    assert not any(
        result.document_id == "HR-RW-001"
        and result.version == "1.0"
        for result in results
    ), (
        "Superseded HR-RW-001 version 1.0 "
        "was incorrectly returned."
    )

    print("\n" + "=" * 70)
    print("VERSION-AWARE RETRIEVAL PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()