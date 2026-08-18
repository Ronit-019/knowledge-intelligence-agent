from fastapi import FastAPI, HTTPException

from api.dependencies import build_knowledge_query_service
from api.schemas import (
    HealthResponse,
    QueryRequest,
    QueryResponse,
    SourceResponse,
)

app = FastAPI(
    title="Knowledge Intelligence API",
    description="Grounded knowledge retrieval and question answering API.",
    version="1.0.0",
)


knowledge_query_service = None


@app.on_event("startup")
def startup() -> None:
    """
    Build the knowledge-query pipeline when the API starts.
    """

    global knowledge_query_service

    knowledge_query_service = (
        build_knowledge_query_service()
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
) -> QueryResponse:
    """
    Ask a question against the active knowledge base.
    """

    if knowledge_query_service is None:
        raise HTTPException(
            status_code=503,
            detail="Knowledge base is not initialized.",
        )

    try:
        result = knowledge_query_service.ask(
            request.query
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
                score=source.score,
            )
            for source in result.sources.results
        ],
    )
