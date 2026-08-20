from api.dependencies import build_knowledge_application


QUERIES = [
    ("How long can an employee work from another country?", "HR-RW-001"),
    ("What is the maximum duration for international remote work?", "HR-RW-001"),
    ("What approval is required for international remote work?", "HR-RW-001"),
    ("Can employees work remotely after completing probation?", "HR-RW-001"),
    ("What are the rules for international work?", "HR-IW-002"),
    ("What is required before working from another country?", "HR-IW-002"),
    ("What happens if international work exceeds the allowed period?", "HR-IW-002"),
    ("What are the requirements for accessing company systems?", "SEC-ACC-004"),
    ("What does the access and authentication security standard require?", "SEC-ACC-004"),
    ("What security controls apply to employee authentication?", "SEC-ACC-004"),
    ("What are the company's data retention requirements?", "CMP-DH-005"),
    ("How long should company data be retained?", "CMP-DH-005"),
    ("What is the company's data handling policy?", "CMP-DH-005"),
    ("What is the employee expense reimbursement policy?", "FIN-EXP-003"),
    ("How can employees get reimbursed for business expenses?", "FIN-EXP-003"),
    ("What are the rules for submitting employee expenses?", "FIN-EXP-003"),
    ("What is the company's maternity leave policy?", None),
    ("What is the company's dental insurance policy?", None),
    ("What is the company's stock option policy?", None),
    ("What is the company's relocation bonus?", None),
]


def main():
    app = build_knowledge_application()
    retrieval = app.query_service.retrieval_service
    reranker = app.query_service.reranking_service    

    print("=" * 80)
    print("CROSS-ENCODER RERANKING DIAGNOSTICS")
    print("=" * 80)

    for query, expected in QUERIES:
        results = retrieval.search(query=query)

        reranked = reranker.rerank(
            query=query,
            results=results,
            top_k=5,
        )

        print("\n" + "-" * 80)
        print("QUERY")
        print("-" * 80)
        print(query)
        print(f"Expected: {expected}")

        if not reranked:
            print("No results")
            continue

        print("\nRERANKED RESULTS")

        for rank, result in enumerate(reranked, start=1):
            print(
                f"{rank}. "
                f"semantic={result.semantic_score:.4f} | "
                f"rerank={result.rerank_score:.4f} | "
                f"{result.document_id} | "
                f"{result.title}"
            )

        top_score = reranked[0].rerank_score

        second_score = (
            reranked[1].rerank_score
            if len(reranked) > 1
            else None
        )

        margin = (
            top_score - second_score
            if second_score is not None
            else None
        )

        print(
            f"\nTop rerank score: {top_score:.4f}"
        )

        if margin is not None:
            print(
                f"Top-vs-second margin: {margin:.4f}"
            )


if __name__ == "__main__":
    main()
