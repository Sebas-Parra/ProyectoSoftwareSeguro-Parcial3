from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from models.user_model import User

async def get_all_users(db: AsyncSession, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    
    # Contar total (solo activos)
    count_stmt = select(func.count()).select_from(User).filter(User.status == True)
    total = await db.scalar(count_stmt)

    # Obtener usuarios (solo activos)
    stmt = select(User).filter(User.status == True).offset(offset).limit(limit)
    result = await db.execute(stmt)
    users = result.scalars().all()

    return {
        "data": [{
            "id": u.id, "username": u.username, "created_at": u.created_at, "status": u.status,
            "created_by": u.created_by, "updated_at": u.updated_at, "updated_by": u.updated_by
        } for u in users],
        "page": page, "limit": limit, "total": total,
        "total_pages": (total + limit - 1) // limit if total > 0 else 0
    }

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id, User.status == True))
    return result.scalars().first()

async def get_user_by_name(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username, User.status == True))
    return result.scalars().first()

async def get_user_roles(db: AsyncSession, user_id: int):
    stmt = select(User).options(joinedload(User.roles)).filter(User.id == user_id, User.status == True)
    result = await db.execute(stmt)
    user = result.unique().scalars().first()

    if user:
        return [{"id": r.id, "name": r.name, "icon": r.icon, "description": r.description} 
                for r in user.roles if r.status == True]
    return []

async def insert_user(db: AsyncSession, username: str, password: str, created_by: int, updated_by: int):
    existing_user = await get_user_by_name(db, username)
    if existing_user:
        raise ValueError("El nombre de usuario ya está en uso.")

    new_user = User(username=username, password=password, created_by=created_by, updated_by=updated_by)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def update_user(db: AsyncSession, user_id: int, username: str, password: str, updated_by: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado.")

    existing_user = await db.execute(select(User).filter(User.username == username, User.id != user_id, User.status == True))
    if existing_user.scalars().first():
        raise ValueError("El nombre de usuario ya está en uso.")

    user.username = username
    user.password = password
    user.updated_by = updated_by
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int, updated_by: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado.")

    user.status = False
    user.updated_by = updated_by
    await db.commit()
    return user