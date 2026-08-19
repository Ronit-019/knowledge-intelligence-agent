from pydantic import BaseModel, Field, field_validator


class QueryRequest(BaseModel):
    """
    Request body for knowledge queries.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Question to ask the knowledge base.",
        examples=[
            "How long can an employee work from another country?"
        ],
    )

    @field_validator("query")
    @classmethod
    def validate_query(
        cls,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Query cannot be empty."
            )

        return value


class SourceResponse(BaseModel):
    """
    Traceable evidence source returned with an answer.
    """

    document_id: str
    title: str
    version: str
    page: int
    score: float
    chunk_id: str


class QueryResponse(BaseModel):
    """
    Final API response for a knowledge query.
    """

    query: str
    answer: str
    grounded: bool
    source_count: int
    sources: list[SourceResponse]


class DocumentResponse(BaseModel):
    """
    Represents an active knowledge-base document version.
    """

    document_id: str
    title: str
    department: str
    document_type: str
    version: str
    effective_date: str
    status: str
    page: int


class DocumentsResponse(BaseModel):
    """
    Active documents currently available to the API.
    """

    count: int
    documents: list[DocumentResponse]


class HealthResponse(BaseModel):
    """
    API health response.
    """

    status: str