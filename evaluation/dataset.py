from evaluation.models import RetrievalTestCase


RETRIEVAL_TEST_CASES = [

    # ---------------------------------------------------------
    # HR-RW-001
    # ---------------------------------------------------------

    RetrievalTestCase(
        query="How long can an employee work from another country?",
        expected_document_id="HR-RW-001",
    ),

    RetrievalTestCase(
        query="What is the maximum duration for international remote work?",
        expected_document_id="HR-RW-001",
    ),

    RetrievalTestCase(
        query="What approval is required for international remote work?",
        expected_document_id="HR-RW-001",
    ),

    RetrievalTestCase(
        query="Can employees work remotely after completing probation?",
        expected_document_id="HR-RW-001",
    ),

    # ---------------------------------------------------------
    # HR-IW-002
    # ---------------------------------------------------------

    RetrievalTestCase(
        query="What are the rules for international work?",
        expected_document_id="HR-IW-002",
    ),

    RetrievalTestCase(
        query="What is required before working from another country?",
        expected_document_id="HR-IW-002",
    ),

    RetrievalTestCase(
        query="What happens if international work exceeds the allowed period?",
        expected_document_id="HR-IW-002",
    ),

    # ---------------------------------------------------------
    # SEC-ACC-004
    # ---------------------------------------------------------

    RetrievalTestCase(
        query="What are the requirements for accessing company systems?",
        expected_document_id="SEC-ACC-004",
    ),

    RetrievalTestCase(
        query="What does the access and authentication security standard require?",
        expected_document_id="SEC-ACC-004",
    ),

    RetrievalTestCase(
        query="What security controls apply to employee authentication?",
        expected_document_id="SEC-ACC-004",
    ),

    # ---------------------------------------------------------
    # CMP-DH-005
    # ---------------------------------------------------------

    RetrievalTestCase(
        query="What are the company's data retention requirements?",
        expected_document_id="CMP-DH-005",
    ),

    RetrievalTestCase(
        query="How long should company data be retained?",
        expected_document_id="CMP-DH-005",
    ),

    RetrievalTestCase(
        query="What is the company's data handling policy?",
        expected_document_id="CMP-DH-005",
    ),

    # ---------------------------------------------------------
    # FIN-EXP-003
    # ---------------------------------------------------------

    RetrievalTestCase(
        query="What is the employee expense reimbursement policy?",
        expected_document_id="FIN-EXP-003",
    ),

    RetrievalTestCase(
        query="How can employees get reimbursed for business expenses?",
        expected_document_id="FIN-EXP-003",
    ),

    RetrievalTestCase(
        query="What are the rules for submitting employee expenses?",
        expected_document_id="FIN-EXP-003",
    ),

    # ---------------------------------------------------------
    # NEGATIVE / UNANSWERABLE
    # ---------------------------------------------------------

    RetrievalTestCase(
        query="What is the company's maternity leave policy?",
        expected_document_id=None,
    ),

    RetrievalTestCase(
        query="What is the company's dental insurance policy?",
        expected_document_id=None,
    ),

    RetrievalTestCase(
        query="What is the company's stock option policy?",
        expected_document_id=None,
    ),

    RetrievalTestCase(
        query="What is the company's relocation bonus?",
        expected_document_id=None,
    ),
]