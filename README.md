# Knowledge Intelligence Agent

Evidence-grounded enterprise knowledge intelligence using retrieval-augmented generation (RAG).

A production-oriented knowledge assistant that retrieves relevant information from enterprise-style documents, reranks the retrieved evidence, generates grounded answers, maintains conversational context, and abstains when sufficient evidence is unavailable.

## Status

🚀 **V1 — Deployed**

The current V1 implementation includes:

- PDF document ingestion
- Document normalization and chunking
- Metadata-aware document registry
- Semantic vector retrieval
- Sentence Transformer embeddings
- Cross-encoder reranking
- Evidence selection
- Version-aware retrieval
- Grounded LLM answer generation
- Conversational query contextualization
- Abstention when evidence is insufficient
- Retrieval evaluation
- FastAPI inference API
- Streamlit chat interface
- Dockerized deployment
- Google Cloud Run deployment

---

## Live Deployment

### Streamlit Interface

https://knowledge-intelligence-ui-531604065619.asia-south1.run.app

### FastAPI Backend

https://knowledge-intelligence-agent-531604065619.asia-south1.run.app

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | API health check |
| `/documents` | GET | List indexed knowledge-base documents |
| `/query` | POST | Ask a question against the knowledge base |

Interactive API documentation is available through FastAPI at:

```text
/docs
```

---

## What It Does

The Knowledge Intelligence Agent is designed around a simple principle:

> **Retrieve evidence first. Generate the answer second.**

Instead of allowing the LLM to answer directly from its general knowledge, the system first searches the internal knowledge base, reranks the retrieved evidence, selects relevant evidence, and provides that evidence to the answer-generation layer.

If sufficient evidence cannot be found, the system abstains rather than presenting an unsupported answer as fact.

A typical request follows this pipeline:

```text
User Question
      │
      ▼
Conversation Context
      │
      ▼
Semantic Retrieval
      │
      ▼
Cross-Encoder Reranking
      │
      ▼
Evidence Selection
      │
      ▼
Grounded Prompt
      │
      ▼
LLM Generation
      │
      ▼
Grounded Answer
```

---

# Architecture

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
                       FAISS Index
                            │
                            ▼
                    Semantic Retrieval
                            │
                            ▼
                   Cross-Encoder Reranking
                            │
                            ▼
                    Evidence Selection
                            │
                            ▼
                 Conversation Context
                            │
                            ▼
                  Grounded Prompt Builder
                            │
                            ▼
                       Groq LLM
                            │
                            ▼
                   Grounded Answer
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
             Evidence              Abstention
```

---

# Knowledge Base

The current demonstration knowledge base contains **5 enterprise-style policy and security documents** covering:

- Compliance
- Finance
- Human Resources
- Security
- Remote work
- International work
- Employee expenses
- Data handling
- Access and authentication security

The documents are intentionally structured to test:

- Multi-document retrieval
- Metadata-aware retrieval
- Document version handling
- Active-version preference
- Evidence selection
- Conversational follow-up questions
- Unsupported-query rejection

---

# Retrieval Evaluation

The retrieval system was evaluated using a **16-query evaluation set** containing supported and unsupported queries.

### Results

| Metric | Result |
|--------|--------|
| Rank-1 retrieval | **15/16 — 93.75%** |
| Rank-3 retrieval | **15/16 — 93.75%** |
| Mean Reciprocal Rank (MRR) | **0.9375** |
| Unsupported queries correctly rejected | **4/4 — 100%** |
| Rejection accuracy | **100%** |
| False positives | **0** |

The evaluation is designed to measure retrieval quality separately from answer generation quality.

This separation makes it possible to determine whether a failure comes from:

1. Retrieval
2. Reranking
3. Evidence selection
4. Prompt construction
5. LLM generation

rather than treating the complete RAG pipeline as a single black box.

---

# Core Design Principles

## 1. Evidence First

Answers are generated from retrieved evidence rather than relying on unsupported model knowledge.

## 2. Provenance

Retrieved information remains associated with its document metadata, including:

- Document ID
- Document title
- Version
- Page
- Chunk ID

This allows retrieved evidence to be traced back to its source.

## 3. Version Awareness

The knowledge base supports multiple document versions.

When multiple versions exist, retrieval can prioritize the appropriate active version instead of blindly returning outdated content.

## 4. Reranking

Semantic retrieval provides an initial candidate set.

A cross-encoder then evaluates the relevance between the user query and retrieved document chunks before evidence is selected for answer generation.

## 5. Abstention

The system does not assume that every question can be answered.

When retrieved evidence is insufficient, the system returns an explicit abstention response instead of fabricating an answer.

## 6. Conversational Context

Follow-up questions can use previous conversation history to contextualize the current query.

For example:

```text
User:
What is the remote work policy?

Assistant:
The Remote Work Policy allows...

User:
How long can it be approved?

Assistant:
International remote work can be approved for up to 90 consecutive
calendar days...
```

The conversation history is used for context, while the retrieved documents remain the source of truth.

## 7. Independent Evaluation

Retrieval quality and answer generation are evaluated independently.

This makes the system easier to debug and improve as the architecture evolves.

---

# Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## Retrieval & RAG

- LangChain Core
- LangChain Text Splitters
- FAISS
- Sentence Transformers
- BGE embeddings
- Cross-Encoder reranking
- NumPy

## Document Processing

- PyMuPDF
- PyMuPDF4LLM
- LangChain document processing

## LLM

- Groq
- Configurable LLM provider architecture

## Frontend

- Streamlit
- Requests

## Infrastructure

- Docker
- Google Cloud Run
- Google Artifact Registry

## Testing

- Pytest

---

# Project Structure

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
├── scripts/
│   └── generate_demo_pdfs.py
│
├── Dockerfile
├── Dockerfile.ui
├── requirements.txt
├── requirements-api.txt
├── requirements-ui.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Configuration

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

**Never commit API keys or other secrets to the repository.**

---

# Installation

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
source .venv/Scripts/activate
```

Install the development dependencies:

```bash
pip install -r requirements.txt
```

---

# Running Locally

## Start the API

```bash
uvicorn api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Start the Streamlit Interface

Set the API URL:

### Git Bash

```bash
export KNOWLEDGE_API_URL="http://127.0.0.1:8000"
```

Then start Streamlit:

```bash
streamlit run frontend/app.py
```

---

# Running the Frontend Against the Deployed API

The Streamlit frontend can also communicate with the deployed FastAPI service.

```bash
export KNOWLEDGE_API_URL="https://knowledge-intelligence-agent-531604065619.asia-south1.run.app"
```

Then:

```bash
streamlit run frontend/app.py
```

---

# API Usage

## Health Check

```bash
curl https://knowledge-intelligence-agent-531604065619.asia-south1.run.app/health
```

Response:

```json
{
  "status": "ok"
}
```

---

## List Documents

```bash
curl https://knowledge-intelligence-agent-531604065619.asia-south1.run.app/documents
```

The endpoint returns the currently indexed documents and their metadata.

---

## Ask a Question

```bash
curl -X POST \
  https://knowledge-intelligence-agent-531604065619.asia-south1.run.app/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the remote work policy?",
    "history": []
  }'
```

The response contains:

- User query
- Generated answer
- Grounding status
- Source count
- Retrieved source metadata
- Semantic retrieval scores
- Reranking scores when available

Example response structure:

```json
{
  "query": "What is the remote work policy?",
  "answer": "...",
  "grounded": true,
  "source_count": 5,
  "sources": []
}
```

---

# Testing

Run the complete test suite:

```bash
python -m pytest -q
```

The project contains tests covering:

- Document ingestion
- PDF processing
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
- Knowledge pipeline behavior

---

# Docker

The API and frontend are deployed as separate containers.

## API

Build:

```bash
docker build -t knowledge-intelligence-agent:v1 .
```

Run:

```bash
docker run --rm \
  -p 8080:8080 \
  -e GROQ_API_KEY="your_groq_api_key" \
  knowledge-intelligence-agent:v1
```

## Streamlit UI

Build:

```bash
docker build \
  -f Dockerfile.ui \
  -t knowledge-intelligence-ui:v1 .
```

Run:

```bash
docker run --rm \
  -p 8501:8080 \
  -e KNOWLEDGE_API_URL="http://host.docker.internal:8000" \
  knowledge-intelligence-ui:v1
```

---

# Cloud Deployment

The current architecture uses two independent Google Cloud Run services.

```text
                    Internet
                       │
                       ▼
        ┌─────────────────────────┐
        │ Streamlit UI            │
        │ Cloud Run               │
        │ knowledge-intelligence- │
        │ ui                      │
        └────────────┬────────────┘
                     │
                     │ HTTPS
                     ▼
        ┌─────────────────────────┐
        │ FastAPI Backend         │
        │ Cloud Run               │
        │ knowledge-intelligence- │
        │ agent                   │
        └─────────────────────────┘
```

This separation allows the frontend and backend to be deployed and scaled independently.

### Current Services

**Frontend**

```text
knowledge-intelligence-ui
```

**Backend**

```text
knowledge-intelligence-agent
```

Both services are deployed in:

```text
asia-south1
```

Container images are stored in Google Artifact Registry.

---

# Security Considerations

The project is designed around enterprise knowledge retrieval, where document provenance and access boundaries are important.

The current implementation keeps API credentials outside the source code through environment-based configuration.

Future production hardening will include:

- Secret Manager integration
- Authentication
- Authorization
- Document-level access control
- Permission-aware retrieval
- Audit logging
- Request tracing
- Sensitive-data handling
- Rate limiting
- Network security controls

---

# Current Limitations

V1 intentionally focuses on establishing a reliable RAG foundation.

The following capabilities are **not yet implemented**:

- Hybrid keyword + semantic retrieval
- LangGraph-based agentic retrieval
- Multi-step tool-using agents
- Citation validation
- Document-level authorization
- User authentication
- Persistent conversational memory
- Production observability
- Automated document ingestion pipeline
- Answer-quality evaluation at scale

These are planned for future iterations.

---

# Development Roadmap

## Reliable RAG Foundation

- [x] Project structure
- [x] PDF ingestion
- [x] Document normalization
- [x] Chunking
- [x] Embedding generation
- [x] Vector retrieval
- [x] Document registry
- [x] Version-aware retrieval
- [x] Active document handling
- [x] Evidence selection
- [x] Cross-encoder reranking
- [x] Abstention logic
- [x] Retrieval evaluation
- [x] FastAPI API
- [x] Streamlit interface
- [x] Dockerized API
- [x] Dockerized frontend
- [x] Google Cloud Run deployment

---

# Engineering Focus

The project is intentionally being developed incrementally.

Rather than starting with an autonomous agent and adding retrieval around it, the implementation first establishes reliable foundations:

```text
Retrieval
   ↓
Reranking
   ↓
Evidence Selection
   ↓
Grounded Generation
   ↓
Evaluation
   ↓
Agentic Retrieval
```

The goal is to make each layer measurable before increasing system complexity.

This allows future agentic behavior to be evaluated against a known retrieval and grounding baseline.

---

# License

This project is currently intended as a personal engineering project and research/learning implementation.