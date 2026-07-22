from sqlalchemy.orm import Session
from repositories import sale_repository
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all_sales_service(db: Session, page: int = 1, limit: int = 10):
    return await sale_repository.get_all_sales(db, page, limit)

async def create_sale_service(db: Session, name: str, description: str, total: float, created_by: int, updated_by: int):
    return await sale_repository.insert_sale(db, name, description, total, created_by, updated_by)

async def update_sale_service(db: AsyncSession, sale_id: int, name: str, description: str, total: float, updated_by: int):
    return await sale_repository.update_sale(db, sale_id, name, description, total, updated_by)

async def delete_sale_service(db: Session, sale_id: int, updated_by: int):
    await sale_repository.delete_sale(db, sale_id, updated_by)
