from dataclasses import dataclass

from ingestion.models import KnowledgeDocument

from services.answer_generation_service import (
    AnswerGenerationService,
    GeneratedAnswer,
)
from services.chunking_service import DocumentChunker
from services.evidence_selector import EvidenceSelector
from services.indexing_service import (
    IndexingResult,
    IndexingService,
)
from services.ingestion_service import IngestionService
from services.retrieval_service import RetrievalService


@dataclass(frozen=True)
class KnowledgeBaseBuildResult:
    """
    Represents the result of building the searchable
    knowledge base.
    """

    documents_ingested: int
    chunks_created: int
    indexing_result: IndexingResult


class KnowledgePipeline:
    """
    End-to-end knowledge intelligence pipeline.

    Responsibilities:
    - Build the searchable knowledge base
    - Retrieve evidence for user questions
    - Select final evidence
    - Generate grounded answers
    """

    def __init__(
        self,
        ingestion_service: IngestionService,
        chunker: DocumentChunker,
        indexing_service: IndexingService,
        retrieval_service: RetrievalService,
        evidence_selector: EvidenceSelector,
        answer_generation_service: AnswerGenerationService,
    ):
        self.ingestion_service = ingestion_service
        self.chunker = chunker
        self.indexing_service = indexing_service
        self.retrieval_service = retrieval_service
        self.evidence_selector = evidence_selector
        self.answer_generation_service = (
            answer_generation_service
        )

    def build_knowledge_base(
        self,
        knowledge_base_path: str,
    ) -> KnowledgeBaseBuildResult:
        """
        Ingest, chunk, embed, and index the knowledge base.
        """

        documents = self.ingestion_service.ingest(
            knowledge_base_path
        )

        if not documents:
            raise ValueError(
                "Knowledge base produced no documents."
            )

        chunks = []

        for document in documents:
            document_chunks = self.chunker.chunk(
                document
            )

            chunks.extend(document_chunks)

        if not chunks:
            raise ValueError(
                "Knowledge base produced no chunks."
            )

        indexing_result = self.indexing_service.index(
            chunks
        )

        return KnowledgeBaseBuildResult(
            documents_ingested=len(documents),
            chunks_created=len(chunks),
            indexing_result=indexing_result,
        )

    def ask(
        self,
        query: str,
        top_k: int = 5,
    ) -> GeneratedAnswer:
        """
        Retrieve evidence and generate a grounded answer.
        """

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        retrieval_results = self.retrieval_service.search(
            query=query,
            top_k=top_k,
        )

        evidence = self.evidence_selector.select(
            retrieval_results
        )

        return self.answer_generation_service.generate(
            query=query,
            evidence=evidence,
        )