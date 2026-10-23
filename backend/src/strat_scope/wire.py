"""Strict edge-only transport models, including the WS envelope schema."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

type ExactInteger = Annotated[str, Field(pattern=r"^-?(0|[1-9][0-9]*)$", max_length=40)]
type ExactDecimal = Annotated[
    str, Field(pattern=r"^-?(0|[1-9][0-9]*)(\.[0-9]+)?$", max_length=100)
]


class WireModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class ExactObservation(WireModel):
    instant: ExactInteger
    unit: Literal["ns", "ms"]
    occurrence: ExactInteger
    value: ExactDecimal


class Capability(WireModel):
    token: str
    epoch: str
    purpose: Literal["foundation-status"] = "foundation-status"
    expires_in_seconds: Literal[300] = 300


class Authentication(WireModel):
    token: Annotated[str, Field(max_length=100)]
    epoch: Annotated[str, Field(max_length=100)]
    purpose: Literal["foundation-status"]


class UpdateEnvelope(WireModel):
    kind: Literal["foundation-status"] = "foundation-status"
    epoch: str
    status: Literal["infrastructure-ready"] = "infrastructure-ready"
    business_features: Literal["not-implemented"] = "not-implemented"
