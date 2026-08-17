import faiss
import numpy as np

from langchain_core.documents import Document


class VectorStore:
    """
    Local vector index for semantic document retrieval.

    Stores:
    - embedding vectors in FAISS
    - original LangChain Documents in memory

    The document metadata remains attached to each vector so
    retrieved results can be traced back to the source document.
    """

    def __init__(self, dimension: int):
        if dimension <= 0:
            raise ValueError("Embedding dimension must be positive.")

        self.dimension = dimension

        # Inner-product search works with normalized embeddings
        # and is equivalent to cosine similarity.
        self.index = faiss.IndexFlatIP(dimension)

        self.documents: list[Document] = []

    def add(
        self,
        embeddings: list[list[float]],
        documents: list[Document],
    ) -> None:
        """Add document embeddings to the vector index."""

        if not embeddings:
            raise ValueError("Cannot add empty embeddings.")

        if len(embeddings) != len(documents):
            raise ValueError(
                "Number of embeddings must match number of documents."
            )

        vectors = np.array(
            embeddings,
            dtype="float32",
        )

        if vectors.ndim != 2 or vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected vectors with dimension {self.dimension}, "
                f"received shape {vectors.shape}."
            )

        self.index.add(vectors)
        self.documents.extend(documents)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[tuple[Document, float]]:
        """
        Search for the most semantically similar documents.

        Returns:
            List of (Document, similarity_score)
        """

        if not self.documents:
            raise ValueError("Vector store is empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        query = np.array(
            [query_embedding],
            dtype="float32",
        )

        if query.shape[1] != self.dimension:
            raise ValueError(
                f"Expected query dimension {self.dimension}, "
                f"received {query.shape[1]}."
            )

        actual_k = min(top_k, len(self.documents))

        scores, indices = self.index.search(
            query,
            actual_k,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            document = self.documents[int(index)]
            results.append(
                (document, float(score))
            )

        return results

    @property
    def size(self) -> int:
        """Return number of indexed documents."""

        return self.index.ntotal