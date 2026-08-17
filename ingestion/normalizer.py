import hashlib
import re

from langchain_core.documents import Document

from ingestion.models import KnowledgeDocument


class DocumentNormalizer:
    """
    Normalize LangChain PDF documents into application documents.

    The normalizer converts loader-specific Document objects into
    the application's stable KnowledgeDocument model while preserving
    document identity, versioning, provenance, and content integrity.
    """

    FIELD_PATTERNS = {
        "document_id": r"\*\*Document ID:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z][A-Za-z ]*:\*\*|$)",
        "department": r"\*\*Department:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z][A-Za-z ]*:\*\*|$)",
        "document_type": r"\*\*Document Type:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z][A-Za-z ]*:\*\*|$)",
        "version": r"\*\*Version:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z][A-Za-z ]*:\*\*|$)",
        "effective_date": r"\*\*Effective Date:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z][A-Za-z ]*:\*\*|$)",
        "status": r"\*\*Status:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z][A-Za-z ]*:\*\*|$)",
        "source": r"\*\*Source:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z][A-Za-z ]*:\*\*|$)",
    }

    def normalize(
        self,
        document: Document,
    ) -> KnowledgeDocument:
        """
        Convert one LangChain Document into a KnowledgeDocument.
        """

        metadata = self._resolve_metadata(document)

        content = self._clean_content(
            document.page_content
        )

        content_hash = hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

        return KnowledgeDocument(
            document_id=metadata["document_id"],
            title=metadata["title"],
            department=metadata["department"],
            document_type=metadata["document_type"],
            version=metadata["version"],
            effective_date=metadata["effective_date"],
            status=metadata["status"],
            source=metadata["source"],
            supersedes=metadata.get("supersedes"),
            page=document.metadata.get("page", 0) + 1,
            content=content,
            content_hash=content_hash,
        )

    def _resolve_metadata(
        self,
        document: Document,
    ) -> dict[str, str]:
        """
        Resolve metadata from native PDF metadata and structured
        metadata embedded in the document content.
        """

        text = document.page_content

        metadata: dict[str, str] = {}

        # ---------------------------------------------------------
        # Native PDF metadata
        # ---------------------------------------------------------

        native_title = document.metadata.get("title")

        if native_title:
            metadata["title"] = str(
                native_title
            ).strip()

        # ---------------------------------------------------------
        # Structured Markdown metadata
        # ---------------------------------------------------------

        for field, pattern in self.FIELD_PATTERNS.items():
            match = re.search(
                pattern,
                text,
                flags=re.DOTALL,
            )

            if match:
                value = self._clean_metadata_value(
                    match.group(1)
                )

                if value:
                    metadata[field] = value

        # ---------------------------------------------------------
        # Supersedes
        #
        # This is intentionally handled separately because it is
        # commonly the final metadata field before the document
        # content begins.
        # ---------------------------------------------------------

        supersedes_match = re.search(
            r"\*\*Supersedes:\*\*\s*([^\n]+)",
            text,
        )

        if supersedes_match:
            supersedes = self._clean_metadata_value(
                supersedes_match.group(1)
            )

            if supersedes:
                metadata["supersedes"] = supersedes

        # ---------------------------------------------------------
        # Fallback title
        # ---------------------------------------------------------

        if not metadata.get("title"):
            title_match = re.search(
                r"^#\s+\*\*(.*?)\*\*",
                text,
                flags=re.MULTILINE,
            )

            if title_match:
                metadata["title"] = (
                    title_match.group(1).strip()
                )

        # ---------------------------------------------------------
        # Validate required metadata
        # ---------------------------------------------------------

        required = {
            "document_id",
            "title",
            "department",
            "document_type",
            "version",
            "effective_date",
            "status",
            "source",
        }

        missing = sorted(
            required - metadata.keys()
        )

        if missing:
            raise ValueError(
                "Missing required document metadata: "
                + ", ".join(missing)
            )

        return metadata

    @staticmethod
    def _clean_metadata_value(
        value: str,
    ) -> str:
        """
        Clean extracted metadata without modifying its meaning.
        """

        value = value.strip()

        value = value.replace(
            r"\:",
            ":",
        )

        return value

    @staticmethod
    def _clean_content(
        text: str,
    ) -> str:
        """
        Normalize whitespace while preserving document structure.
        """

        text = re.sub(
            r"\n+",
            "\n",
            text,
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        return text.strip()