import math

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
        if not isinstance(dimension, int):
            raise TypeError("Embedding dimension must be an integer.")

        if dimension <= 0:
            raise ValueError(
                "Embedding dimension must be positive."
            )

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
        """
        Add document embeddings to the vector index.
        """

        if not embeddings:
            raise ValueError(
                "Cannot add empty embeddings."
            )

        if not documents:
            raise ValueError(
                "Cannot add embeddings without documents."
            )

        if len(embeddings) != len(documents):
            raise ValueError(
                "Number of embeddings must match "
                "number of documents."
            )

        vectors = np.asarray(
            embeddings,
            dtype="float32",
        )

        if vectors.ndim != 2:
            raise ValueError(
                "Embeddings must be a two-dimensional matrix."
            )

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected vectors with dimension "
                f"{self.dimension}, "
                f"received shape {vectors.shape}."
            )

        if not np.isfinite(vectors).all():
            raise ValueError(
                "Embeddings contain non-finite values."
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
            raise ValueError(
                "Vector store is empty."
            )

        if not isinstance(top_k, int):
            raise TypeError(
                "top_k must be an integer."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        query = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        if query.ndim != 2:
            raise ValueError(
                "Query embedding must be a one-dimensional vector."
            )

        if query.shape[1] != self.dimension:
            raise ValueError(
                f"Expected query dimension "
                f"{self.dimension}, "
                f"received {query.shape[1]}."
            )

        if not np.isfinite(query).all():
            raise ValueError(
                "Query embedding contains non-finite values."
            )

        actual_k = min(
            top_k,
            self.size,
        )

        scores, indices = self.index.search(
            query,
            actual_k,
        )

        results: list[tuple[Document, float]] = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):
            # FAISS can return -1 for missing neighbours
            # in some index configurations.
            if index < 0:
                continue

            score = float(score)

            if not math.isfinite(score):
                continue

            document = self.documents[int(index)]

            results.append(
                (document, score)
            )

        return results

    def clear(self) -> None:
        """
        Remove all indexed vectors and documents.
        """

        self.index.reset()
        self.documents.clear()

    @property
    def size(self) -> int:
        """
        Return number of indexed documents.
        """

        return self.index.ntotal