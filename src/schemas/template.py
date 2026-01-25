# src/schemas/template.py
from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Literal, Optional

SlotType = Literal["string", "number", "boolean", "list_string"]


class TemplateMeta(BaseModel):
    """
    Metadata associated with a Template.

    This model contains system-level and collaboration-related information
    that is not directly tied to the template's content or structure.
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
        description="Primary author of the template",
    )
    collaborators: list[str] = Field(
        default_factory=list,
        description="List of collaborators involved in the template",
    )


class TemplateSlot(BaseModel):
    """
    Defines a single input slot required by a Template.

    Each slot represents one piece of structured input that the user
    must (or may) provide when instantiating the template.
    """

    name: str = Field(
        ...,
        description="Unique slot identifier within the template",
    )
    required: bool = Field(
        default=True,
        description="Whether this slot is required for validation",
    )
    type: SlotType = Field(
        default="string",
        description="Expected data type of the slot",
    )
    description: str = Field(
        default="",
        description="Human-readable description of the slot",
    )
    example: Optional[str] = Field(
        default=None,
        description="Example value used for prompting or UI hints",
    )


class Template(BaseModel):
    """
    Canonical definition of a document Template.

    A Template defines:
    - its identity and version
    - a set of input slots required to generate a document
    - metadata for auditing and collaboration
    """

    template_id: str = Field(
        ...,
        description="Unique, stable identifier for the template",
    )
    display_name: str = Field(
        ...,
        description="Human-readable name shown to users",
    )
    version: str = Field(
        ...,
        description="Version identifier of the template",
    )
    slots: list[TemplateSlot] = Field(
        default_factory=list,
        description="Definitions of input slots used by the template",
    )
    metadata: TemplateMeta = Field(
        default_factory=TemplateMeta,
        description="Metadata associated with the template",
    )

    def required_slots(self) -> list[str]:
        """
        Return the names of all required slots.

        Useful for validating user input against the template definition.
        """
        return [s.name for s in self.slots if s.required]

    def slot_map(self) -> dict[str, TemplateSlot]:
        """
        Return a mapping of slot name to TemplateSlot definition.

        Enables fast lookup of slot metadata during validation
        or document generation.
        """
        return {s.name: s for s in self.slots}
