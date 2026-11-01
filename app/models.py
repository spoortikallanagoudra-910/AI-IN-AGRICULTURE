from typing import Any, Literal

from pydantic import BaseModel, Field


class FarmContext(BaseModel):
    farm_name: str | None = None
    location: str | None = None
    crop: str | None = None
    variety: str | None = None
    growth_stage: str | None = None
    field_size_ha: float | None = Field(default=None, gt=0)
    soil_type: str | None = None
    soil_ph: float | None = Field(default=None, ge=0, le=14)
    weather: dict[str, Any] = Field(default_factory=dict)
    variables: dict[str, Any] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)
    domain: Literal[
        "crop_management",
        "livestock",
        "vision",
        "soil_water",
        "pest_disease",
        "market",
        "weather",
        "farm_business",
        "sustainability",
        "general",
    ] = "general"
    context: FarmContext = Field(default_factory=FarmContext)


class SafetyFinding(BaseModel):
    category: str
    severity: Literal["info", "warning", "critical"]
    message: str


class ChatResponse(BaseModel):
    answer: str
    domain: str
    mode: Literal["live", "demo"]
    safety_findings: list[SafetyFinding] = Field(default_factory=list)
    follow_up_questions: list[str] = Field(default_factory=list)
    disclaimer: str = (
        "This prototype provides decision support, not a substitute for a "
        "licensed agronomist, veterinarian, extension specialist, or other "
        "qualified professional."
    )
