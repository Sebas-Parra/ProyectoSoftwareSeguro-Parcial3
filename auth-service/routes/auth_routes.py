from fastapi import APIRouter, Depends, Security, Request
from sqlalchemy.orm import Session
from config.database import get_db
from controllers import auth_controller
from dtos.auth_dto import RegisterDTO, LoginDTO, SelectRoleDTO
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.rate_limit import limiter

security = HTTPBearer()
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/select-role")
async def select_role(data: SelectRoleDTO, db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Security(security)):
    return await auth_controller.select_role_controller(db, data, token)

@router.post("/login")
@limiter.limit("5/1minutes")
async def login(request: Request, data: LoginDTO, db: Session = Depends(get_db)):
    return await auth_controller.login_controller(db, data)

@router.post("/refresh-token")
async def refresh_token(token: HTTPAuthorizationCredentials = Security(security)):
    return await auth_controller.refresh_token_controller(token)

@router.post("/logout")
async def logout(token: HTTPAuthorizationCredentials = Security(security)):
    return await auth_controller.logout_controller(token)