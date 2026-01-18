# src/schemas/document.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Literal, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID

DocumentStatus = Literal["draft", "validated", "final"]


class DocumentMeta(BaseModel):
    """
    문서의 공통 필드 (Create, Update, Read에서 공유)
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC creation time",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC last update time",
    )
    author: str = Field(default_factory=list, description="Primary author")
    collaborators: List[str] = Field(
        default_factory=list, description="Collaborators on the document"
    )


class Document(BaseModel):
    doc_id: UUID = Field(..., description="Unique document id")
    template_id: Optional[UUID] = Field(
        ..., description="Template id used for the document"
    )
    title: str = Field(..., description="Title of the document")
    fields: Dict[str, Any] = Field(
        default_factory=dict, description="Template fields(flat-friendly)"
    )
    metadata: DocumentMeta = Field(
        default_factory=DocumentMeta, description="Metadata of the document"
    )
    status: DocumentStatus = Field(default="draft")

    def touch(self) -> None:
        self.metadata.updated_at = datetime.now(timezone.utc)
