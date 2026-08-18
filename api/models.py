from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """
    Request body for the knowledge query endpoint.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask the knowledge base.",
    )


class SourceResponse(BaseModel):
    """
    Source metadata returned with an answer.
    """

    document_id: str
    title: str
    version: str
    page: int
    score: float
    chunk_id: str


class QueryResponse(BaseModel):
    """
    API response for a knowledge query.
    """

    answer: str
    grounded: bool
    sources: list[SourceResponse]