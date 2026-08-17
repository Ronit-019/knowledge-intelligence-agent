from pathlib import Path

from langchain_pymupdf4llm import PyMuPDF4LLMLoader

from ingestion.models import KnowledgeDocument
from ingestion.normalizer import DocumentNormalizer


class IngestionService:
    """
    Loads and normalizes knowledge-base PDFs.

    Responsibilities:
    - Discover PDF documents recursively
    - Load PDFs using LangChain's PyMuPDF4LLM integration
    - Normalize extracted documents
    - Preserve document metadata and provenance
    """

    def __init__(
        self,
        normalizer: DocumentNormalizer,
    ):
        self.normalizer = normalizer

    def discover_pdfs(
        self,
        knowledge_base_path: str | Path,
    ) -> list[Path]:
        """
        Recursively discover PDF files in the knowledge base.
        """

        root = Path(knowledge_base_path)

        if not root.exists():
            raise FileNotFoundError(
                f"Knowledge base does not exist: {root}"
            )

        if not root.is_dir():
            raise ValueError(
                f"Knowledge base path is not a directory: {root}"
            )

        pdfs = sorted(
            root.rglob("*.pdf")
        )

        if not pdfs:
            raise ValueError(
                f"No PDF documents found in: {root}"
            )

        return pdfs

    def load_pdf(
        self,
        pdf_path: str | Path,
    ) -> list[KnowledgeDocument]:
        """
        Load and normalize one PDF.
        """

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF does not exist: {pdf_path}"
            )

        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Expected a PDF file: {pdf_path}"
            )

        loader = PyMuPDF4LLMLoader(
            str(pdf_path)
        )

        documents = loader.load()

        normalized_documents = []

        for document in documents:
            normalized = self.normalizer.normalize(
                document
            )

            normalized_documents.append(
                normalized
            )

        return normalized_documents

    def ingest(
        self,
        knowledge_base_path: str | Path,
    ) -> list[KnowledgeDocument]:
        """
        Discover and ingest every PDF in the knowledge base.
        """

        pdf_paths = self.discover_pdfs(
            knowledge_base_path
        )

        normalized_documents = []

        for pdf_path in pdf_paths:
            documents = self.load_pdf(
                pdf_path
            )

            normalized_documents.extend(
                documents
            )

        return normalized_documents