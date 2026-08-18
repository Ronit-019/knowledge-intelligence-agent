from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    Request body for knowledge queries.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Question to ask the knowledge base.",
    )


class SourceResponse(BaseModel):
    """
    Traceable evidence source returned with an answer.
    """

    document_id: str
    title: str
    version: str
    page: int
    score: float


class QueryResponse(BaseModel):
    """
    Final API response for a knowledge query.
    """

    query: str
    answer: str
    grounded: bool
    source_count: int
    sources: list[SourceResponse]


class HealthResponse(BaseModel):
    """
    API health response.
    """

    status: str
