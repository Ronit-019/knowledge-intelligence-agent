from pathlib import Path

from langchain_pymupdf4llm import PyMuPDF4LLMLoader

from ingestion.normalizer import DocumentNormalizer
from ingestion.chunker import DocumentChunker
from services.embedding_service import EmbeddingService
from services.indexing_service import IndexingService
from services.retrieval_service import RetrievalService
from services.evidence_selector import EvidenceSelector
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

        for document in loader.load():
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

    return RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        similarity_threshold=0.65,
    )


def main():

    print("=" * 70)
    print("EVIDENCE SELECTION")
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

    retrieved = retrieval_service.search(
        query=query,
        top_k=10,
    )

    print(
        f"\nRetrieved candidates: "
        f"{len(retrieved)}"
    )

    selector = EvidenceSelector(
        max_results=5,
        max_chunks_per_document=2,
    )

    selection = selector.select(
        retrieved
    )

    print("\n" + "-" * 70)
    print("SELECTED EVIDENCE")
    print("-" * 70)

    for rank, result in enumerate(
        selection.results,
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

    assert selection.count <= 5

    document_counts = {}

    for result in selection.results:
        document_counts[result.document_id] = (
            document_counts.get(
                result.document_id,
                0,
            ) + 1
        )

    assert all(
        count <= 2
        for count in document_counts.values()
    ), (
        "Evidence selector allowed too many "
        "chunks from one document."
    )

    assert any(
        result.document_id == "HR-RW-001"
        for result in selection.results
    ), (
        "Expected Remote Work Policy evidence "
        "was not selected."
    )

    print("\n" + "=" * 70)
    print("EVIDENCE SELECTION PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()