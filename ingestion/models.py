from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeDocument:
    document_id: str
    title: str
    department: str
    document_type: str
    version: str
    effective_date: str
    status: str
    source: str
    supersedes: str | None
    page: int
    content: str
    content_hash: str