from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from controllers import menu_controller
from dtos.menu_dto import MenuCreateDTO, MenuUpdateDTO, MenuResponseDTO
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

security = HTTPBearer()
router = APIRouter(prefix="/api/menus", tags=["Menus"])

@router.get("/tree", response_model=List[MenuResponseDTO])
async def get_active_menus(
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await menu_controller.get_active_menus_flat_controller(db, token)

@router.get("")
async def get_all_menus(
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await menu_controller.get_all_menus_controller(db, token)

@router.post("", response_model=MenuResponseDTO, status_code=201)
async def create_menu(
    menu_data: MenuCreateDTO,
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await menu_controller.create_menu_controller(db, menu_data, token)

@router.put("/{menu_id}", response_model=MenuResponseDTO)
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdateDTO,
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await menu_controller.update_menu_controller(db, menu_id, menu_data, token)

@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: int,
    db: AsyncSession = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await menu_controller.delete_menu_controller(db, menu_id, token)