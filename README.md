# Knowledge Intelligence Agent

Evidence-grounded enterprise knowledge intelligence using agentic RAG.

## Status

🚧 Phase 1 — Foundation

## Goal

Build an AI system that can retrieve information from enterprise-style
documents, reason across multiple sources, provide verifiable citations,
and abstain when sufficient evidence is unavailable.

## Planned Capabilities

- Document ingestion
- Metadata-aware chunking
- Hybrid retrieval
- Reranking
- Agentic retrieval with LangGraph
- Evidence-grounded generation
- Citation validation
- Abstention
- Retrieval evaluation
- Answer-quality evaluation
- FastAPI inference API
- Streamlit interface
- Production observability

## Architecture

```text
Enterprise Documents
        │
        ▼
Document Ingestion
        │
        ▼
Normalization
        │
        ▼
Metadata-Aware Chunking
        │
        ▼
Embedding Generation
        │
        ▼
Vector Store
        │
        ▼
Retrieval
        │
        ▼
Reranking
        │
        ▼
Evidence Selection
        │
        ▼
Agentic Reasoning
        │
        ▼
Evidence-Grounded Answer
        │
        ├── Citations
        └── Abstention
```

## Project Structure

```text
knowledge-intelligence-agent/
│
├── api/
│   ├── dependencies.py
│   ├── main.py
│   └── schemas.py
│
├── config/
│   └── settings.py
│
├── evaluation/
│   ├── dataset.py
│   ├── evaluator.py
│   └── models.py
│
├── frontend/
│   └── app.py
│
├── ingestion/
│   ├── chunker.py
│   ├── models.py
│   └── normalizer.py
│
├── registry/
│   └── document_registry.py
│
├── retrieval/
│   └── vector_store.py
│
├── services/
│   ├── answer_generation_service.py
│   ├── chunking_service.py
│   ├── conversation_service.py
│   ├── embedding_service.py
│   ├── evidence_selector.py
│   ├── indexing_service.py
│   ├── ingestion_service.py
│   ├── knowledge_base_service.py
│   ├── knowledge_pipeline.py
│   ├── knowledge_query_service.py
│   ├── prompt_builder.py
│   ├── reranking_service.py
│   ├── retrieval_service.py
│   └── llm/
│       ├── base.py
│       └── groq_provider.py
│
├── tests/
│
├── data/
│   └── knowledge_base/
│       ├── compliance/
│       ├── finance/
│       ├── hr/
│       └── security/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Knowledge Base

The current knowledge base contains enterprise-style policy documents
covering areas such as:

- Compliance
- Finance
- Human Resources
- Security
- Remote work
- International work
- Employee expenses
- Data handling
- Access security

The documents are intentionally structured to support multi-document
retrieval, version-aware retrieval, evidence selection, and abstention.

## Core Design Principles

### 1. Evidence First

The system should generate answers from retrieved evidence rather than
relying on unsupported model knowledge.

### 2. Provenance

Retrieved information should remain traceable to the original document
and its metadata.

### 3. Version Awareness

When multiple versions of a document exist, retrieval should prefer the
appropriate active version instead of blindly returning outdated content.

### 4. Reranking

Initial semantic retrieval should be followed by a stronger relevance
ranking stage before evidence is selected for answer generation.

### 5. Abstention

The system should refuse to provide a definitive answer when the
available evidence is insufficient or unreliable.

### 6. Evaluation

Retrieval and answer generation should be evaluated independently so that
weak retrieval can be distinguished from weak generation.

## Technology Stack

### Backend

- Python
- FastAPI
- Pydantic

### Retrieval & RAG

- LangChain
- FAISS
- Sentence Transformers
- BGE embeddings
- Cross-encoder reranking

### Document Processing

- PyMuPDF4LLM
- LangChain document loaders

### LLM

- Groq
- Configurable LLM provider architecture

### Frontend

- Streamlit

### Testing

- Pytest

## Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key

LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-20b

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

TOP_K=10
RERANK_TOP_K=5
MIN_RERANK_SCORE=-3.0

ENVIRONMENT=development
LOG_LEVEL=INFO
```

The `.env` file is intentionally excluded from Git.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI application with:

```bash
uvicorn api.main:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Running the Frontend

Start the Streamlit interface with:

```bash
streamlit run frontend/app.py
```

## Testing

Run the test suite with:

```bash
python -m pytest -q
```

The project contains tests covering:

- Document ingestion
- Document normalization
- Chunking
- Embeddings
- Vector retrieval
- Version-aware retrieval
- Active document handling
- Evidence selection
- Reranking
- Prompt construction
- Answer generation
- Abstention
- Retrieval evaluation
- API dependencies

## Evaluation

The evaluation layer is designed to measure retrieval quality independently
from answer generation.

Current evaluation areas include:

- Retrieval relevance
- Retrieval diagnostics
- Reranking diagnostics
- Abstention thresholds
- Answer generation behavior

## Development Roadmap

- [x] Project structure
- [x] PDF ingestion
- [x] Document normalization
- [x] Chunking
- [x] Embedding generation
- [x] Vector retrieval
- [x] Document registry
- [x] Version-aware retrieval
- [x] Evidence selection
- [x] Reranking
- [x] Abstention logic
- [x] Initial evaluation framework
- [x] FastAPI foundation
- [x] Streamlit foundation


## Security Considerations

The project is designed around enterprise knowledge retrieval, where
document provenance and access boundaries are important.

Future production work will include:

- Authentication
- Authorization
- Document-level access control
- Secure secret management
- Audit logging
- Request tracing
- Sensitive-data handling
- Permission-aware retrieval

## Current Objective

The immediate objective is to establish a reliable RAG foundation before
adding more complex agentic behavior.

The system should first demonstrate that it can:

1. Ingest enterprise documents.
2. Preserve document metadata.
3. Retrieve relevant evidence.
4. Rerank retrieved information.
5. Select high-quality evidence.
6. Generate answers grounded in that evidence.
7. Cite the source information.
8. Abstain when evidence is insufficient.
9. Measure retrieval and answer quality.

Only after these foundations are reliable should the system move toward
fully agentic retrieval and multi-step reasoning.

## License

This project is currently intended as a personal engineering project and
research/learning implementation.