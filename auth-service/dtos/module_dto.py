from pydantic import BaseModel 

class ModuleDTO(BaseModel):
    name: str
    description: str
    icon: str
    status: bool