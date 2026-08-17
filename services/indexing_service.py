from dataclasses import dataclass

from langchain_core.documents import Document

from services.embedding_service import EmbeddingService
from retrieval.vector_store import VectorStore


@dataclass(frozen=True)
class IndexingResult:
    """
    Represents the result of indexing a collection of documents.
    """

    documents_indexed: int
    embedding_dimension: int


class IndexingService:
    """
    Builds a searchable vector index from document chunks.

    Responsibilities:
    - Generate embeddings for chunks
    - Add embeddings to the vector store
    - Keep indexing logic separate from retrieval logic
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index(
        self,
        documents: list[Document],
    ) -> IndexingResult:
        """
        Embed and index a collection of LangChain Documents.
        """

        if not documents:
            raise ValueError(
                "Cannot index an empty document collection."
            )

        texts = [
            document.page_content
            for document in documents
        ]

        embeddings = self.embedding_service.embed_documents(
            texts
        )

        self.vector_store.add(
            embeddings=embeddings,
            documents=documents,
        )

        return IndexingResult(
            documents_indexed=len(documents),
            embedding_dimension=self.embedding_service.dimension,
        )