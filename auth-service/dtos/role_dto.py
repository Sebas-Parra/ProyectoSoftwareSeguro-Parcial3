from pydantic import BaseModel 

class RoleDTO(BaseModel):
    name: str
    description: str
    icon: str
    status: bool