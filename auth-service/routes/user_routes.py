from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session
from config.database import get_db
from controllers import user_controller
from dtos.auth_dto import RegisterDTO
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()
router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("")
async def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await user_controller.get_all_users_controller(db, page, limit, token)

@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await user_controller.get_user_by_id_controller(db, user_id, token)

@router.post("")
async def register_user(
    data: RegisterDTO,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await user_controller.register_user_controller(db, data.username, data.password, token)

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    data: RegisterDTO,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security)
):
    return await user_controller.update_user_controller(db, user_id, data.username, data.password, token)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Security(security),
):
    return await user_controller.delete_user_controller(db, user_id, token)
