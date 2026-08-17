from dataclasses import dataclass

from services.retrieval_service import RetrievalResult


@dataclass(frozen=True)
class EvidenceSelection:
    """
    Represents the final evidence selected for answer generation.
    """

    results: list[RetrievalResult]

    @property
    def count(self) -> int:
        return len(self.results)


class EvidenceSelector:
    """
    Selects diverse, relevant evidence from retrieval results.

    The selector:
    - Preserves retrieval relevance
    - Avoids excessive duplicate chunks from one document
    - Keeps multiple documents when they provide useful evidence
    """

    def __init__(
        self,
        max_results: int = 5,
        max_chunks_per_document: int = 2,
    ):
        if max_results <= 0:
            raise ValueError(
                "max_results must be greater than zero."
            )

        if max_chunks_per_document <= 0:
            raise ValueError(
                "max_chunks_per_document must be greater than zero."
            )

        self.max_results = max_results
        self.max_chunks_per_document = (
            max_chunks_per_document
        )

    def select(
        self,
        results: list[RetrievalResult],
    ) -> EvidenceSelection:
        """
        Select final evidence from ranked retrieval results.
        """

        if not results:
            return EvidenceSelection(
                results=[]
            )

        selected = []
        document_counts: dict[str, int] = {}

        for result in results:

            document_id = result.document_id

            current_count = document_counts.get(
                document_id,
                0,
            )

            if (
                current_count
                >= self.max_chunks_per_document
            ):
                continue

            selected.append(result)

            document_counts[document_id] = (
                current_count + 1
            )

            if len(selected) >= self.max_results:
                break

        return EvidenceSelection(
            results=selected
        )