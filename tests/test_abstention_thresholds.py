from api.dependencies import build_knowledge_application


QUERIES = [
    ("How long can an employee work remotely from another country?", "HR-RW-001"),
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


THRESHOLDS = [
    -10,
    -9,
    -8,
    -7,
    -6,
    -5,
    -4,
    -3.5,
    -3,
    -2.5,
    -2,
    -1.5,
    -1,
    -0.5,
    0,
]


def main():
    app = build_knowledge_application()

    retrieval = app.query_service.retrieval_service
    reranker = app.query_service.reranking_service

    print("=" * 80)
    print("RERANK ABSTENTION THRESHOLD SWEEP")
    print("=" * 80)

    results = []

    for query, expected in QUERIES:
        retrieved = retrieval.search(query=query)

        reranked = reranker.rerank(
            query=query,
            results=retrieved,
            top_k=5,
        )

        top_score = (
            reranked[0].rerank_score
            if reranked
            else None
        )

        top_document = (
            reranked[0].document_id
            if reranked
            else None
        )

        results.append(
            (
                query,
                expected,
                top_score,
                top_document,
            )
        )

    print()

    for threshold in THRESHOLDS:

        supported_correct = 0
        supported_total = 0
        rejected_correct = 0
        false_positives = 0

        for query, expected, score, document_id in results:

            accepted = (
                score is not None
                and score >= threshold
            )

            if expected is None:
                if accepted:
                    false_positives += 1
                else:
                    rejected_correct += 1

            else:
                supported_total += 1

                if accepted and document_id == expected:
                    supported_correct += 1

        print(
            f"threshold={threshold:>6.1f} | "
            f"supported={supported_correct}/{supported_total} | "
            f"correct_rejections={rejected_correct}/4 | "
            f"false_positives={false_positives}/4"
        )


if __name__ == "__main__":
    main()