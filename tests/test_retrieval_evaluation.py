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


def main():
    app = build_knowledge_application()

    retrieval = app.query_service.retrieval_service
    reranker = app.query_service.reranking_service

    hit_at_1 = 0
    hit_at_3 = 0
    reciprocal_rank_sum = 0.0

    correct_rejections = 0
    false_positives = 0

    failures = []

    print("=" * 80)
    print("RETRIEVAL + RERANKING EVALUATION")
    print("=" * 80)

    for query, expected in QUERIES:

        results = retrieval.search(query=query)

        reranked = reranker.rerank(
            query=query,
            results=results,
            top_k=5,
        )

        document_ids = [
            result.document_id
            for result in reranked
        ]

        # --------------------------------------------------
        # Out-of-domain query
        # --------------------------------------------------

        if expected is None:

            if not reranked:
                correct_rejections += 1
                status = "PASS - correctly rejected"
            else:
                false_positives += 1
                status = "FAIL - false positive"

                failures.append(
                    {
                        "query": query,
                        "expected": None,
                        "actual": document_ids,
                        "top_score": reranked[0].rerank_score,
                    }
                )

            print(
                f"\n[{status}]"
            )
            print(query)

            if reranked:
                print(
                    f"Top: {document_ids[0]} "
                    f"| score={reranked[0].rerank_score:.4f}"
                )

            continue

        # --------------------------------------------------
        # In-domain query
        # --------------------------------------------------

        rank = None

        for index, document_id in enumerate(
            document_ids,
            start=1,
        ):
            if document_id == expected:
                rank = index
                break

        if rank == 1:
            hit_at_1 += 1

        if rank is not None and rank <= 3:
            hit_at_3 += 1

        if rank is not None:
            reciprocal_rank_sum += 1.0 / rank

        if rank is None:
            failures.append(
                {
                    "query": query,
                    "expected": expected,
                    "actual": document_ids,
                    "top_score": (
                        reranked[0].rerank_score
                        if reranked
                        else None
                    ),
                }
            )

        status = (
            f"PASS - rank {rank}"
            if rank is not None
            else "FAIL"
        )

        print(
            f"\n[{status}]"
        )
        print(query)
        print(f"Expected: {expected}")
        print(f"Results: {document_ids}")

    total_supported = sum(
        1
        for _, expected in QUERIES
        if expected is not None
    )

    total_queries = len(QUERIES)

    mrr = (
        reciprocal_rank_sum / total_supported
        if total_supported
        else 0.0
    )

    hit1 = (
        hit_at_1 / total_supported
        if total_supported
        else 0.0
    )

    hit3 = (
        hit_at_3 / total_supported
        if total_supported
        else 0.0
    )

    rejection_rate = (
        correct_rejections
        / (correct_rejections + false_positives)
        if (correct_rejections + false_positives)
        else 0.0
    )

    print("\n")
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(
        f"Supported queries : {total_supported}"
    )

    print(
        f"Total queries     : {total_queries}"
    )

    print(
        f"Hit@1             : {hit_at_1}/{total_supported} "
        f"({hit1:.2%})"
    )

    print(
        f"Hit@3             : {hit_at_3}/{total_supported} "
        f"({hit3:.2%})"
    )

    print(
        f"MRR               : {mrr:.4f}"
    )

    print(
        f"Correct rejections: {correct_rejections}"
    )

    print(
        f"False positives   : {false_positives}"
    )

    print(
        f"Rejection accuracy: {rejection_rate:.2%}"
    )

    print(
        f"Failures          : {len(failures)}"
    )

    if failures:

        print("\n")
        print("=" * 80)
        print("FAILURES")
        print("=" * 80)

        for failure in failures:
            print(
                f"\nQuery: {failure['query']}"
            )
            print(
                f"Expected: {failure['expected']}"
            )
            print(
                f"Actual: {failure['actual']}"
            )
            print(
                f"Top score: {failure['top_score']}"
            )


if __name__ == "__main__":
    main()