from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from controllers import role_controller
from controllers import menu_controller
from controllers import module_controller

from dtos.role_dto import RoleDTO
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter(prefix="/api/roles", tags=["Roles"])

@router.post("/{menu_id}/menus/{role_id}", status_code=200)
async def assign_menu_to_role(
    menu_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await menu_controller.insert_role_menu_controller(db, role_id, menu_id, token)



@router.post("/{module_id}/modules/{role_id}")
async def assign_module_to_role(
    module_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await module_controller.assign_module_to_role_controller(db, role_id, module_id, token)


@router.get("")
async def get_roles(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await role_controller.get_all_roles_controller(db, token)

@router.put("/{role_id}")
async def update_role(
    role_id: int,
    role_data: RoleDTO,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await role_controller.update_role_controller(db, role_id, role_data, token)


@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await role_controller.delete_role_controller(db, role_id, token)


@router.post("/{role_id}/user/{user_id}")
async def assign_role_to_user(
    role_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await role_controller.asign_role_to_user_controller(db, user_id, role_id, token)

@router.delete("/{role_id}/user/{user_id}")
async def desasign_role_from_user(
    role_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await role_controller.desasign_role_from_user_controller(db, user_id, role_id, token)

@router.post("")
async def insert_role(
    role_data: RoleDTO,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await role_controller.insert_role_controller(db, role_data, token)