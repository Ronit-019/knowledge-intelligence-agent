from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from services.conversation_service import (
    ConversationMessage,
)
from api.dependencies import (
    KnowledgeApplication,
    build_knowledge_application,
)
from api.schemas import (
    DocumentResponse,
    DocumentsResponse,
    HealthResponse,
    QueryRequest,
    QueryResponse,
    SourceResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize the knowledge intelligence application
    when the API starts.
    """

    app.state.knowledge_application = (
        build_knowledge_application()
    )

    yield

    # Reserved for future cleanup:
    # vector stores, database connections,
    # model resources, etc.


app = FastAPI(
    title="Knowledge Intelligence API",
    description=(
        "Grounded knowledge retrieval and question answering API."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:
    """
    API health check.
    """

    return HealthResponse(
        status="ok"
    )


@app.post(
    "/query",
    response_model=QueryResponse,
)
def query(
    request: QueryRequest,
    http_request: Request,
) -> QueryResponse:
    """
    Ask a question against the active knowledge base.
    """

    application: KnowledgeApplication | None = getattr(
        http_request.app.state,
        "knowledge_application",
        None,
    )

    if application is None:
        raise HTTPException(
            status_code=503,
            detail="Knowledge base is not initialized.",
        )

    try:
        history = [
            ConversationMessage(
                role=message.role,
                content=message.content,
            )
            for message in request.history
        ]

        result = application.query_service.ask(
            query=request.query,
            history=history,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return QueryResponse(
        query=result.query,
        answer=result.answer,
        grounded=result.grounded,
        source_count=result.source_count,
        sources=[
            SourceResponse(
                document_id=source.document_id,
                title=source.title,
                version=source.version,
                page=source.page,
                semantic_score=source.semantic_score,
                rerank_score=source.rerank_score,
                chunk_id=source.chunk_id,
            )
            for source in result.sources.results
        ],
    )


@app.get(
    "/documents",
    response_model=DocumentsResponse,
)
def documents(
    http_request: Request,
) -> DocumentsResponse:
    """
    Return the active documents currently indexed
    in the knowledge base.
    """

    application: KnowledgeApplication | None = getattr(
        http_request.app.state,
        "knowledge_application",
        None,
    )

    if application is None:
        raise HTTPException(
            status_code=503,
            detail="Knowledge base is not initialized.",
        )

    active_documents = (
        application.knowledge_base.documents
    )

    return DocumentsResponse(
        count=len(active_documents),
        documents=[
            DocumentResponse(
                document_id=document.document_id,
                title=document.title,
                department=document.department,
                document_type=document.document_type,
                version=document.version,
                effective_date=document.effective_date,
                status=document.status,
                page=document.page,
            )
            for document in active_documents
        ],
    )