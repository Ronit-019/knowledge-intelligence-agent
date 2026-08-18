from ingestion.models import KnowledgeDocument


class DocumentRegistry:
    """
    In-memory registry for knowledge documents and their versions.

    The registry keeps track of every ingested document version
    and identifies which version is currently active.
    """

    def __init__(self):
        self._documents: dict[
            str,
            list[KnowledgeDocument],
        ] = {}

    def register(
        self,
        document: KnowledgeDocument,
    ) -> None:
        """
        Register a document version.
        """

        versions = self._documents.setdefault(
            document.document_id,
            [],
        )

        for existing in versions:
            if existing.version == document.version:
                raise ValueError(
                    f"Document version already registered: "
                    f"{document.document_id}:{document.version}"
                )

        versions.append(document)

    def register_many(
        self,
        documents: list[KnowledgeDocument],
    ) -> None:
        """
        Register multiple document versions.
        """

        for document in documents:
            self.register(document)

    def get_versions(
        self,
        document_id: str,
    ) -> list[KnowledgeDocument]:
        """
        Return all registered versions of a document.
        """

        return list(
            self._documents.get(
                document_id,
                [],
            )
        )

    def get_active(
        self,
        document_id: str,
    ) -> KnowledgeDocument | None:
        """
        Return the active version of a document.
        """

        versions = self.get_versions(document_id)

        active_versions = [
            document
            for document in versions
            if document.status.lower() == "active"
        ]

        if not active_versions:
            return None

        if len(active_versions) > 1:
            raise ValueError(
                f"Multiple active versions found for "
                f"document: {document_id}"
            )

        return active_versions[0]

    def is_active(
        self,
        document_id: str,
        version: str,
    ) -> bool:
        """
        Check whether a specific document version is active.
        """

        active = self.get_active(document_id)

        if active is None:
            return False

        return active.version == version
    
    def get_active_documents(self) -> list[KnowledgeDocument]:
        """
        Return every currently active document version.
        """

        active_documents = []

        for document_id in self._documents:
            active = self.get_active(document_id)

            if active is not None:
                active_documents.append(active)

        return active_documents

    @property
    def size(self) -> int:
        """
        Return total number of registered document versions.
        """

        return sum(
            len(versions)
            for versions in self._documents.values()
        )