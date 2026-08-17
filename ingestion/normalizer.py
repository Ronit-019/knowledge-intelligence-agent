import hashlib
import re

from langchain_core.documents import Document

from ingestion.models import KnowledgeDocument


class DocumentNormalizer:
    """Normalize LangChain PDF documents into application documents."""

    FIELD_PATTERNS = {
        "document_id": r"\*\*Document ID:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z ]+:\*\*|$)",
        "department": r"\*\*Department:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z ]+:\*\*|$)",
        "document_type": r"\*\*Document Type:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z ]+:\*\*|$)",
        "version": r"\*\*Version:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z ]+:\*\*|$)",
        "effective_date": r"\*\*Effective Date:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z ]+:\*\*|$)",
        "status": r"\*\*Status:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z ]+:\*\*|$)",
        "source": r"\*\*Source:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z ]+:\*\*|$)",
        "supersedes": r"\*\*Supersedes:\*\*\s*(.*?)(?=\s+\*\*[A-Za-z ]+:\*\*|$)",
    }

    def normalize(
        self,
        document: Document,
    ) -> KnowledgeDocument:

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

        text = document.page_content

        metadata = {}

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
                value = match.group(1).strip()

                value = value.replace(
                    r"\:",
                    ":",
                )

                metadata[field] = value

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
        # Validate
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
    def _clean_content(
        text: str,
    ) -> str:

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