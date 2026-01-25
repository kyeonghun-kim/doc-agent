# src/schemas/document.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

DocumentStatus = Literal["draft", "validated", "final"]


class DocumentMeta(BaseModel):
    """
    Metadata associated with a Document.

    Contains system-level information such as timestamps
    and collaboration-related data.
    """

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC creation time",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC last update time",
    )
    author: Optional[str] = Field(
        default=None,
        description="Primary author of the document",
    )
    collaborators: list[str] = Field(
        default_factory=list,
        description="Collaborators on the document",
    )


class Document(BaseModel):
    """
    Represents a concrete document instance created from a Template.

    A Document stores user-provided field values, metadata,
    and its current lifecycle status.
    """

    doc_id: UUID = Field(
        ...,
        description="Unique identifier of the document",
    )

    template_id: Optional[UUID] = Field(
        default=None,
        description="Template identifier used to create the document",
    )

    title: str = Field(
        ...,
        description="Title of the document",
    )

    fields: Dict[str, Any] = Field(
        default_factory=dict,
        description="Flattened key-value pairs corresponding to template slots",
    )

    metadata: DocumentMeta = Field(
        default_factory=DocumentMeta,
        description="Metadata associated with the document",
    )

    status: DocumentStatus = Field(
        default="draft",
        description="Current lifecycle status of the document",
    )

    def touch(self) -> None:
        """
        Update the document's `updated_at` timestamp.

        Should be called whenever the document content or metadata changes.
        """
        self.metadata.updated_at = datetime.now(timezone.utc)
