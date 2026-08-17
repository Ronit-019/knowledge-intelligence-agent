from services.answer_generation_service import (
    AnswerGenerationService,
)
from services.chunking_service import DocumentChunker
from services.embedding_service import EmbeddingService
from services.evidence_selector import EvidenceSelector
from services.indexing_service import IndexingService
from services.ingestion_service import IngestionService
from services.knowledge_pipeline import KnowledgePipeline
from services.llm.groq_provider import GroqProvider
from services.prompt_builder import PromptBuilder
from services.retrieval_service import RetrievalService
from retrieval.vector_store import VectorStore
from ingestion.normalizer import DocumentNormalizer


KNOWLEDGE_BASE_PATH = "data/knowledge_base"


def build_pipeline() -> KnowledgePipeline:

    normalizer = DocumentNormalizer()

    ingestion_service = IngestionService(
        normalizer=normalizer
    )

    chunker = DocumentChunker(
        chunk_size=1000,
        chunk_overlap=150,
    )

    embedding_service = EmbeddingService()

    vector_store = VectorStore(
        dimension=embedding_service.dimension
    )

    indexing_service = IndexingService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
        similarity_threshold=0.65,
    )

    evidence_selector = EvidenceSelector(
        max_results=5,
        max_chunks_per_document=2,
    )

    prompt_builder = PromptBuilder()

    llm_provider = GroqProvider(
        model_name="openai/gpt-oss-20b"
    )

    answer_generation_service = (
        AnswerGenerationService(
            llm_provider=llm_provider,
            prompt_builder=prompt_builder,
        )
    )

    return KnowledgePipeline(
        ingestion_service=ingestion_service,
        chunker=chunker,
        indexing_service=indexing_service,
        retrieval_service=retrieval_service,
        evidence_selector=evidence_selector,
        answer_generation_service=answer_generation_service,
    )


def main():

    print("=" * 70)
    print("END-TO-END KNOWLEDGE PIPELINE")
    print("=" * 70)

    pipeline = build_pipeline()

    print()
    print("-" * 70)
    print("BUILDING KNOWLEDGE BASE")
    print("-" * 70)

    build_result = pipeline.build_knowledge_base(
        KNOWLEDGE_BASE_PATH
    )

    print(
        f"Documents ingested: "
        f"{build_result.documents_ingested}"
    )

    print(
        f"Chunks created: "
        f"{build_result.chunks_created}"
    )

    print(
        f"Documents indexed: "
        f"{build_result.indexing_result.documents_indexed}"
    )

    print(
        f"Embedding dimension: "
        f"{build_result.indexing_result.embedding_dimension}"
    )

    print()
    print("-" * 70)
    print("ASKING QUESTION")
    print("-" * 70)

    query = (
        "How long can an employee work "
        "from another country?"
    )

    print(f"Question: {query}")

    result = pipeline.ask(query)

    print()
    print("-" * 70)
    print("ANSWER")
    print("-" * 70)

    print(result.answer)

    print()
    print("-" * 70)
    print("METADATA")
    print("-" * 70)

    print(f"Grounded: {result.grounded}")
    print(f"Sources: {result.sources.count}")

    for index, source in enumerate(
        result.sources.results,
        start=1,
    ):
        print()
        print(f"Source {index}")
        print(f"  Document: {source.title}")
        print(f"  Document ID: {source.document_id}")
        print(f"  Version: {source.version}")
        print(f"  Page: {source.page}")
        print(f"  Score: {source.score:.4f}")

    assert build_result.documents_ingested == 6
    assert build_result.chunks_created == 12
    assert build_result.indexing_result.documents_indexed == 12

    assert result.grounded is True
    assert result.sources.count > 0
    assert result.answer.strip()

    print()
    print("=" * 70)
    print("END-TO-END PIPELINE TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    main()