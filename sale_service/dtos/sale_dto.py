from pydantic import BaseModel 

class SaleDTO(BaseModel):
    name: str
    description: str
    total: float
    status: bool