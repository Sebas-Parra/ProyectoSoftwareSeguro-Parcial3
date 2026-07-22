from pydantic import BaseModel, Field
from typing import List, Optional

class MenuCreateDTO(BaseModel):
    nombre: str = Field(..., example="Configuración")
    url: Optional[str] = Field(None, example="/api/config")
    modulo_id: int = Field(..., example=1)
    parent_id: Optional[int] = Field(None, description="Null si es raíz", example=None)

class MenuUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, example="Configuración General")
    url: Optional[str] = Field(None, example="/api/config/general")
    parent_id: Optional[int] = Field(None, example=2)
    status: Optional[bool] = Field(None, example=True)

class MenuResponseDTO(BaseModel):
    id: int
    nombre: str
    url: Optional[str]
    modulo_id: int
    parent_id: Optional[int]
    status: bool
    children: List['MenuResponseDTO'] = []

    class Config:
        from_attributes = True

MenuResponseDTO.model_rebuild()