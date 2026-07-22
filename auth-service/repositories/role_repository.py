from sqlalchemy import select, update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from models.role_model import Role
from models.user_roles_model import UserRole

async def get_all_roles(db: AsyncSession):
    result = await db.execute(select(Role))
    return result.scalars().all()

async def insert_role(db: AsyncSession, name: str, description: str, icon: str, created_by: int, updated_by: int):
    new_role = Role(
        name=name,
        icon=icon,
        description=description,
        status=True,
        created_by=created_by,
        updated_by=updated_by
    )
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role

async def update_role(db: AsyncSession, role_id: int, name: str, icon: str, description: str, status: bool, updated_by: int):
    result = await db.execute(select(Role).filter(Role.id == role_id))
    role = result.scalars().first()
    if role:
        role.name = name
        role.icon = icon
        role.description = description
        role.status = status
        role.updated_by = updated_by
        await db.commit()
        await db.refresh(role)
    return role


async def delete_role(db: AsyncSession, role_id: int, updated_by: int):
    result = await db.execute(select(Role).filter(Role.id == role_id, Role.status == True))
    role = result.scalars().first()
    if role:
        role.status = False
        role.updated_by = updated_by
        await db.commit()
        await db.refresh(role)
    return role

async def asign_role_to_user(db: AsyncSession, user_id: int, role_id: int, created_by: int, updated_by: int):
    result = await db.execute(select(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id))
    exist_user_role = result.scalars().first()
    
    if exist_user_role:
        return exist_user_role  

    user_role = UserRole(user_id=user_id, role_id=role_id, created_by=created_by, updated_by=updated_by)
    db.add(user_role)
    await db.commit()
    await db.refresh(user_role)
    return user_role

async def desasign_role_from_user(db: AsyncSession, user_id: int, role_id: int):
    result = await db.execute(select(UserRole).filter(UserRole.user_id == user_id, UserRole.role_id == role_id))
    user_role = result.scalars().first()
    
    if user_role:
        await db.delete(user_role)
        await db.commit()
        return True
    return False







