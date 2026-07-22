from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services import module_service, jwt_service
from fastapi.security import HTTPAuthorizationCredentials

async def get_all_modules_controller(db: AsyncSession, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        modules = await module_service.get_all_modules_service(db)
        return modules
    except Exception as e:
        print(f"Error en get_all_modules_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    
async def insert_module_controller(db: AsyncSession, module_data, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        new_module = await module_service.insert_module_service(
            db, module_data.name, module_data.icon, 
            module_data.description, created_by=int(payload['sub']), updated_by=int(payload['sub'])
        )
        return new_module
    except Exception as e:
        print(f"Error en insert_module_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    
    
async def update_module_controller(db: AsyncSession, module_id: int, module_data, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        await module_service.update_module_service(
            db, module_id, module_data.name, module_data.icon, 
            module_data.description, module_data.status, updated_by=int(payload['sub'])
        )
        return {"message": "Módulo actualizado exitosamente"}
    except Exception as e:
        print(f"Error en update_module_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def delete_module_controller(db: AsyncSession, module_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        deleted_module = await module_service.delete_module_service(db, module_id, updated_by=int(payload['sub']))
        if not deleted_module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Módulo no encontrado"
            )
        return {"message": "Módulo eliminado exitosamente"}
    except Exception as e:
        print(f"Error en delete_module_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def assign_module_to_role_controller(db: AsyncSession, role_id: int, module_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        role_module = await module_service.assign_module_to_role_service(
            db, role_id, module_id, created_by=int(payload['sub']), updated_by=int(payload['sub'])
        )
        return role_module
    except Exception as e:
        print(f"Error en assign_module_to_role_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    