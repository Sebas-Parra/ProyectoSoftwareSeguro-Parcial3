from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services import role_service, jwt_service
from fastapi.security import HTTPAuthorizationCredentials

async def get_all_roles_controller(db: AsyncSession, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        roles = await role_service.get_all_roles_service(db)
        return roles
    except Exception as e:
        print(f"Error en get_all_roles_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    
async def update_role_controller(db: AsyncSession, role_id: int, role_data, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        await role_service.update_role_service(
            db, role_id, role_data.name, role_data.icon, 
            role_data.description, role_data.status, updated_by=int(payload['sub'])
        )
        return {"message": "Rol actualizado exitosamente"}
    except Exception as e:
        print(f"Error en update_role_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def delete_role_controller(db: AsyncSession, role_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        deleted_role = await role_service.delete_role_service(db, role_id, updated_by=int(payload['sub']))
        if not deleted_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        return {"message": "Rol eliminado exitosamente"}
    except Exception as e:
        print(f"Error en delete_role_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def asign_role_to_user_controller(db: AsyncSession, user_id: int, role_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        user_role = await role_service.asign_role_to_user_service(
            db, user_id, role_id, created_by=int(payload['sub']), updated_by=int(payload['sub'])
        )
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario o rol no válido"
            )
        return {"message": "Rol asignado al usuario exitosamente"}
    except Exception as e:
        print(f"Error en asign_role_to_user_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    
async def desasign_role_from_user_controller(db: AsyncSession, user_id: int, role_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        user_role = await role_service.desasign_role_from_user_service(db, user_id, role_id)
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario o rol no válido"
            )
        return {"message": "Rol desasignado del usuario exitosamente"}
    except Exception as e:
        print(f"Error en desasign_role_from_user_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def insert_role_controller(db: AsyncSession, role_data, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        new_role = await role_service.insert_role_service(
            db, role_data.name,  
            role_data.description, role_data.icon, created_by=int(payload['sub']), updated_by=int(payload['sub'])
        )
        return {"message": "Rol insertado exitosamente", "role": new_role}
    except Exception as e:
        print(f"Error en insert_role_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )