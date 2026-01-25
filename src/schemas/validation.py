# src/schemas/validation.py
from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, model_validator


class Severity(str, Enum):
    """
    Severity level of a validation issue.

    - error: Critical issue that makes the document invalid
    - warning: Non-blocking issue that should be reviewed
    - info: Informational notice
    """

    error = "error"
    warning = "warning"
    info = "info"


class ValidationIssue(BaseModel):
    """
    Represents a single validation issue detected during document validation.

    This model is used for missing fields, validation errors, and warnings,
    and can be aggregated into a ValidationResult.
    """

    field_name: str = Field(
        ...,
        description="Name of the field associated with the validation issue",
    )
    message: str = Field(
        ...,
        description="Human-readable description of the validation issue",
    )
    severity: Severity = Field(
        ...,
        description="Severity level of the issue (error, warning, info)",
    )


class ValidationResult(BaseModel):
    """
    Aggregated result of validating a document against a template or schema.

    - `valid` is a derived field and is automatically synchronized based on issues.
    - Missing fields and errors invalidate the document.
    - Warnings do not affect validity.
    """

    valid: bool = Field(
        default=True,
        description="Whether the document is considered valid",
    )

    # Fields that are required but missing from the document
    missing: list[ValidationIssue] = Field(
        default_factory=list,
        description="List of missing required field issues",
    )

    # Other validation errors (type mismatch, constraint violation, etc.)
    errors: list[ValidationIssue] = Field(
        default_factory=list,
        description="List of validation errors",
    )

    # Non-blocking issues that should be reviewed by the user
    warnings: list[ValidationIssue] = Field(
        default_factory=list,
        description="List of validation warnings",
    )

    @model_validator(mode="after")
    def _sync_valid(self) -> "ValidationResult":
        """
        Synchronize the `valid` field based on validation issues.

        A document is considered valid if and only if:
        - there are no missing required fields
        - there are no validation errors

        Warnings do not affect validity.
        """
        self.valid = len(self.missing) == 0 and len(self.errors) == 0
        return self

    def all_issues(self) -> list[ValidationIssue]:
        """
        Return all validation issues in a single list.

        Useful for unified rendering, logging, or reporting.
        """
        return self.missing + self.errors + self.warnings

    def missing_field_names(self) -> list[str]:
        """
        Return the names of all missing required fields.
        """
        return [issue.field_name for issue in self.missing]
