from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from validate_docbr import CPF, CNPJ

cpf_validator = CPF()
cnpj_validator = CNPJ()


class CropInput(BaseModel):
    id: int | None = None
    season: str
    name: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"season": "2023/2024", "name": "Soja"}}
    )


class FarmInput(BaseModel):
    id: int | None = None
    name: str
    city: str
    state: str
    total_area: float
    agricultural_area: float
    vegetation_area: float
    crops: List[CropInput] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Fazenda Santa Maria",
                "city": "Ribeirão Preto",
                "state": "SP",
                "total_area": 150.0,
                "agricultural_area": 90.0,
                "vegetation_area": 60.0,
                "crops": [
                    {"season": "2023/2024", "name": "Soja"},
                    {"season": "2022/2023", "name": "Milho"},
                ],
            }
        }
    )


class ProducerInput(BaseModel):
    name: str
    document: str
    farms: Optional[List[FarmInput]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "José da Silva",
                "document": "123.456.789-09",
                "farms": [
                    {
                        "id": 1,
                        "name": "Fazenda Santa Maria",
                        "city": "Ribeirão Preto",
                        "state": "SP",
                        "total_area": 150.0,
                        "agricultural_area": 90.0,
                        "vegetation_area": 60.0,
                        "crops": [
                            {"id": 1, "season": "2023/2024", "name": "Soja"},
                            {"season": "2022/2023", "name": "Milho"},
                        ],
                    }
                ],
            }
        }
    )

    @field_validator("document")
    @classmethod
    def validate_document(cls, v: str) -> str:
        digits = "".join(filter(str.isdigit, v))
        if len(digits) == 11:
            if not cpf_validator.validate(digits):
                raise ValueError("CPF inválido")
        elif len(digits) == 14:
            if not cnpj_validator.validate(digits):
                raise ValueError("CNPJ inválido")
        else:
            raise ValueError("Documento deve conter 11 (CPF) ou 14 (CNPJ) dígitos")
        return v

    model_config = ConfigDict(from_attributes=True)


class CropOutput(BaseModel):
    id: int
    season: str
    name: str


class FarmOutput(BaseModel):
    id: int
    name: str
    city: str
    state: str
    total_area: float
    agricultural_area: float
    vegetation_area: float
    crops: List[CropOutput]


class ProducerOutput(BaseModel):
    id: int
    name: str
    document: str
    farms: List[FarmOutput]


class ProducerListResponse(BaseModel):
    total: int
    page: int
    size: int
    producers: List[ProducerOutput]
