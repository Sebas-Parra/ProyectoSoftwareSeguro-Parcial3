from polars import datetime
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from models.sale_model import Sale

async def get_all_sales(db: AsyncSession, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    
    # Contar total
    count_stmt = select(func.count()).select_from(Sale)
    total = await db.scalar(count_stmt)
    
    # Obtener ventas
    stmt = select(Sale).offset(offset).limit(limit)
    result = await db.execute(stmt)
    sales = result.scalars().all()

    return {
        "data": [{
            "id": s.id, "name": s.name, "description": s.description, "total": s.total,
            "created_at": s.created_at, "created_by": s.created_by,
            "updated_at": s.updated_at, "updated_by": s.updated_by,
            "status": s.status
        } for s in sales],
        "page": page, "limit": limit, "total": total,
        "total_pages": (total + limit - 1) // limit if total > 0 else 0
    }

async def insert_sale(db: AsyncSession, name: str, description: str, total: float, created_by: int, updated_by: int):
    new_sale = Sale(name=name, description=description, total=total, created_by=created_by, updated_by=updated_by)
    db.add(new_sale)
    await db.commit()
    await db.refresh(new_sale)
    return new_sale

# Repositorio
async def update_sale(db: AsyncSession, sale_id: int, name: str, description: str, total: float, updated_by: int):
    # 1. Buscar si la venta existe
    result = await db.execute(select(Sale).where(Sale.id == sale_id))
    sale = result.scalar_one_or_none()
    
    if not sale:
        return None  # Retorna None si no existe

    # 2. Actualizar los campos
    sale.name = name
    sale.description = description
    sale.total = total
    sale.updated_by = updated_by

    await db.commit()
    await db.refresh(sale)
    return sale 


async def delete_sale(db: AsyncSession, sale_id: int, updated_by: int):
    stmt = update(Sale).where(Sale.id == sale_id).values(status=False, updated_by=updated_by)
    await db.execute(stmt)
    await db.commit()