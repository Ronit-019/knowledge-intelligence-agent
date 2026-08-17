from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Generates semantic embeddings for document chunks.

    The service owns the embedding model so the rest of the
    application does not need to know which embedding model
    is being used.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""

        if not text or not text.strip():
            raise ValueError("Cannot embed empty text.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for multiple documents."""

        if not texts:
            raise ValueError("Cannot embed an empty document list.")

        if any(not text or not text.strip() for text in texts):
            raise ValueError(
                "Document list contains empty text."
            )

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        """Return embedding vector dimension."""

        return self.model.get_embedding_dimension()