from langchain_core.documents import Document

from ingestion.models import KnowledgeDocument
from ingestion.chunker import DocumentChunker


class ChunkingService:
    """
    Converts normalized knowledge documents into
    retrieval-ready LangChain Documents.
    """

    def __init__(
        self,
        chunker: DocumentChunker,
    ):
        self.chunker = chunker

    def chunk_document(
        self,
        document: KnowledgeDocument,
    ) -> list[Document]:
        """
        Chunk one normalized knowledge document.
        """

        return self.chunker.chunk(document)

    def chunk_documents(
        self,
        documents: list[KnowledgeDocument],
    ) -> list[Document]:
        """
        Chunk an entire normalized knowledge corpus.
        """

        if not documents:
            raise ValueError(
                "Cannot chunk an empty document collection."
            )

        chunks: list[Document] = []

        for document in documents:
            document_chunks = self.chunk_document(
                document
            )

            chunks.extend(document_chunks)

        return chunks