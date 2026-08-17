from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingestion.models import KnowledgeDocument


class DocumentChunker:
    """
    Splits normalized knowledge documents into retrieval-ready chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n## ",
                "\n### ",
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def chunk(
        self,
        document: KnowledgeDocument,
    ) -> list[Document]:
        """
        Convert one normalized document into LangChain Documents.
        """

        base_metadata = {
            "document_id": document.document_id,
            "title": document.title,
            "department": document.department,
            "document_type": document.document_type,
            "version": document.version,
            "effective_date": document.effective_date,
            "status": document.status,
            "source": document.source,
            "supersedes": document.supersedes,
            "page": document.page,
            "content_hash": document.content_hash,
        }

        chunks = self.splitter.create_documents(
            texts=[document.content],
            metadatas=[base_metadata],
        )

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = (
                f"{document.document_id}:"
                f"{document.version}:"
                f"{document.page}:"
                f"{index}"
            )

            chunk.metadata["chunk_index"] = index
            chunk.metadata["total_chunks"] = len(chunks)

        return chunks