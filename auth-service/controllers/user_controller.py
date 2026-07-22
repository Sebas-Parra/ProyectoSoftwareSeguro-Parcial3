from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services import user_service, jwt_service
from fastapi.security import HTTPAuthorizationCredentials

async def get_all_users_controller(db: AsyncSession, page: int, limit: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        users = await user_service.get_all_users(db, page, limit)
        return users
    except Exception as e:
        print(f"Error en get_all_users_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    
async def get_user_by_id_controller(db: AsyncSession, user_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        user = await user_service.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user
    except Exception as e:
        print(f"Error en get_user_by_id_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    
async def register_user_controller(db: AsyncSession, username: str, password: str, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        await user_service.register_user_service(db, username, password, int(payload["sub"]), int(payload["sub"]))
        return {"message": "Usuario registrado exitosamente"}
    except Exception as e:
        print(f"Error en register_user_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def update_user_controller(db: AsyncSession, user_id: int, username: str, password: str, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        await user_service.update_user_service(db, user_id, username, password, int(payload["sub"]))
        return {"message": "Usuario actualizado exitosamente"}
    except Exception as e:
        print(f"Error en update_user_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def delete_user_controller(db: AsyncSession, user_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        await user_service.delete_user_service(db, user_id, int(payload["sub"]))
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        print(f"Error en delete_user_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )