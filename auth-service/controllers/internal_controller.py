from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from services import jwt_service


async def validate_token_controller(credentials: HTTPAuthorizationCredentials):
    """Endpoint privado para que otros microservicios validen un JWT contra
    el Master sin implementar su propia verificacion RS256 (estrategia
    'a: Validacion directa' del PDF). No expone datos sensibles del usuario:
    solo confirma validez, user_id y role_id."""
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token(token, "access")

    if error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error)

    return {
        "valid": True,
        "user_id": int(payload["sub"]),
        "role_id": payload.get("role_id"),
    }
