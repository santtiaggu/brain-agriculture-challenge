from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List
from validate_docbr import CPF, CNPJ

cpf_validator = CPF()
cnpj_validator = CNPJ()


class CropInput(BaseModel):
    season: str = Field(..., example="2023/2024")
    name: str = Field(..., example="Soja")


class FarmInput(BaseModel):
    name: str = Field(..., example="Fazenda Santa Maria")
    city: str = Field(..., example="Ribeirão Preto")
    state: str = Field(..., example="SP")
    total_area: float = Field(..., gt=0, example=150.0)
    agricultural_area: float = Field(..., ge=0, example=90.0)
    vegetation_area: float = Field(..., ge=0, example=60.0)
    crops: List[CropInput] = Field(
        default_factory=list,
        example=[
            {"season": "2023/2024", "name": "Soja"},
            {"season": "2022/2023", "name": "Milho"},
        ],
    )


class ProducerInput(BaseModel):
    document: str = Field(..., example="123.456.789-09")
    name: str = Field(..., example="José da Silva")
    farms: List[FarmInput] = Field(
        default_factory=list,
        example=[
            {
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
        ],
    )

    @field_validator("document")
    @classmethod
    def validate_document(cls, v: str) -> str:
        digits = ''.join(filter(str.isdigit, v))
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
