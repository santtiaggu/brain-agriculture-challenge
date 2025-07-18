from pydantic import BaseModel, Field

class PaginationInput(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)
