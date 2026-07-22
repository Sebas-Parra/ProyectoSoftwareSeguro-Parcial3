from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session
from config.database import get_db
from controllers import module_controller
from dtos.module_dto import ModuleDTO
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter(prefix="/api/modules", tags=["Modules"])

@router.get("")
async def get_modules(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await module_controller.get_all_modules_controller(db, token)

@router.put("/{module_id}")
async def update_module(
    module_id: int,
    module_data: ModuleDTO,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await module_controller.update_module_controller(db, module_id, module_data, token)

@router.delete("/{module_id}")
async def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await module_controller.delete_module_controller(db, module_id, token)


@router.post("")
async def insert_module(
    module_data: ModuleDTO,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await module_controller.insert_module_controller(db, module_data, token)

