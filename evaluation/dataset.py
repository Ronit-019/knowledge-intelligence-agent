from evaluation.models import RetrievalTestCase


RETRIEVAL_TEST_CASES = [
    RetrievalTestCase(
        query="How long can an employee work from another country?",
        expected_document_id="HR-RW-001",
    ),
    RetrievalTestCase(
        query="What approval is required for international remote work?",
        expected_document_id="HR-RW-001",
    ),
    RetrievalTestCase(
        query="Can employees work remotely from their registered country?",
        expected_document_id="HR-RW-001",
    ),
    RetrievalTestCase(
        query="What is the company's maternity leave policy?",
        expected_document_id=None,
    ),
    RetrievalTestCase(
        query="What is the company's dental insurance policy?",
        expected_document_id=None,
    ),
]