from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPAuthorizationCredentials
from services import jwt_service, sale_service


async def create_sale_controller(db: AsyncSession, sale_data, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token(token, "access")

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        new_sale = await sale_service.create_sale_service(
            db, sale_data.name, sale_data.description, sale_data.total, created_by=int(payload['sub']), updated_by=int(payload['sub'])
        )
        return new_sale
    except Exception as e:
        print(f"Error en create_sale_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def get_all_sales_controller(db: AsyncSession, page: int, limit: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token(token, "access")

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        sales = await sale_service.get_all_sales_service(db, page, limit)
        return sales
    except Exception as e:
        print(f"Error en get_all_sales_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def update_sale_controller(db: AsyncSession, sale_id: int, sale_data, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token(token, "access")

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        updated_sale = await sale_service.update_sale_service(
            db, sale_id, sale_data.name, sale_data.description, sale_data.total, updated_by=int(payload['sub'])
        )
        if not updated_sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )
        return updated_sale
    except HTTPException as he:
        raise he  # Deja pasar el 404 limpio sin convertirlo en 500
    except Exception as e:
        print(f"Error en update_sale_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

async def delete_sale_controller(db: AsyncSession, sale_id: int, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    payload, error = await jwt_service.verificar_token(token, "access")

    if error:
        raise HTTPException(status_code=401, detail=error)

    try:
        await sale_service.delete_sale_service(db, sale_id, updated_by=int(payload['sub']))
        return {"message": "Venta eliminada exitosamente"}
    except Exception as e:
        print(f"Error en delete_sale_controller: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )