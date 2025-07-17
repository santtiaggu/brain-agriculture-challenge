"""Health schemas implementation."""

from pydantic import BaseModel, ConfigDict


class HealthOutput(BaseModel):
    """Health output schema."""

    status: str
    model_config = ConfigDict(from_attributes=True)
