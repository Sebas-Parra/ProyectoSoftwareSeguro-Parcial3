from fastapi import APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from controllers import internal_controller

security = HTTPBearer()
router = APIRouter(prefix="/api/internals", tags=["Internal"])


@router.post("/validate-token")
async def validate_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    return await internal_controller.validate_token_controller(credentials)
