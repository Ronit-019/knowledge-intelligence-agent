from evaluation.dataset import RETRIEVAL_TEST_CASES
from tests.test_retrieval_evaluation import build_retrieval_service


def main():

    print("=" * 70)
    print("RETRIEVAL DIAGNOSTICS")
    print("=" * 70)

    retrieval_service = build_retrieval_service()

    for test_case in RETRIEVAL_TEST_CASES:

        print()
        print("-" * 70)
        print("QUERY")
        print("-" * 70)
        print(test_case.query)

        # Temporarily bypass the service threshold and inspect
        # the vector store directly.
        query_embedding = (
            retrieval_service.embedding_service.embed_text(
                test_case.query
            )
        )

        results = (
            retrieval_service.vector_store.search(
                query_embedding=query_embedding,
                top_k=10,
            )
        )

        print()
        print(
            f"Expected: "
            f"{test_case.expected_document_id}"
        )

        for rank, (document, score) in enumerate(
            results,
            start=1,
        ):

            print(
                f"{rank:2}. "
                f"{score:.4f} | "
                f"{document.metadata['document_id']} | "
                f"{document.metadata['title']} | "
                f"{document.metadata['chunk_id']}"
            )

    print()
    print("=" * 70)
    print("DIAGNOSTICS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()