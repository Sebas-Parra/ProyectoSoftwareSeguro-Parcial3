from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services import menu_service, jwt_service
from fastapi.security import HTTPAuthorizationCredentials

async def get_active_menus_flat_controller(db: AsyncSession, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    # Cualquier usuario autenticado debe poder cargar el menu de SU rol
    # seleccionado; no solo el administrador (ese era el bug: bloqueaba
    # a cualquier rol distinto de "administrador").
    payload, error = await jwt_service.verificar_token(token, "access")

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        role_id = payload.get("role_id")
        if not role_id:
            raise HTTPException(status_code=400, detail="El token no contiene un role_id válido")

        menus = await menu_service.get_active_menus_flat_service(db, int(role_id))
        return menus
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error en get_active_menus_flat_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def create_menu_controller(db: AsyncSession, menu_data, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        new_menu = await menu_service.create_menu_service(
            db, menu_data.model_dump(), created_by=int(payload['sub'])
        )
        return new_menu
    except Exception as e:
        print(f"Error en create_menu_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def update_menu_controller(db: AsyncSession, menu_id: int, menu_data, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        updated_menu = await menu_service.update_menu_service(
            db, menu_id, menu_data.model_dump(exclude_unset=True), updated_by=int(payload['sub'])
        )
        if not updated_menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menú no encontrado"
            )
        return updated_menu
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error en update_menu_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def delete_menu_controller(db: AsyncSession, menu_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        await menu_service.delete_menu_service(db, menu_id, updated_by=int(payload['sub']))
        return {"message": "Menú eliminado exitosamente"}
    except Exception as e:
        print(f"Error en delete_menu_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def insert_role_menu_controller(db: AsyncSession, role_id: int, menu_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        await menu_service.insert_role_menu_service(db, role_id, menu_id)
        return {"message": "Menú asignado al rol exitosamente"}
    except Exception as e:
        print(f"Error en insert_role_menu_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def get_all_menus_controller(db: AsyncSession, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token_administrador(db, token)

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        menus = await menu_service.get_all_menus_service(db)
        return menus
    except Exception as e:
        print(f"Error en get_all_menus_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )