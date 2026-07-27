from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.role_model import Role
from models.module_model import Module
from models.role_modules_model import RoleModule


async def get_all_modules(db: AsyncSession):
    result = await db.execute(select(Module).filter(Module.status == True))
    return result.scalars().all()


async def get_module_names_by_role(db: AsyncSession, role_id: int) -> list:
    """Nombres de los modulos ACTIVOS asignados a un rol. Se embeben en el
    JWT al seleccionar el rol para que los microservicios hijos (ej.
    sale_service para el modulo "Ventas") puedan autorizar sin consultar
    al Master en cada request."""
    result = await db.execute(
        select(Module.name)
        .join(RoleModule, RoleModule.module_id == Module.id)
        .filter(RoleModule.role_id == role_id, Module.status == True)
    )
    return [name for (name,) in result.all()]


async def insert_module(db: AsyncSession, name: str, icon: str, description: str, created_by: int, updated_by: int):
    new_module = Module(
        name=name,
        icon=icon,
        description=description,
        status=True,
        created_by=created_by,
        updated_by=updated_by
    )
    db.add(new_module)
    await db.commit()
    await db.refresh(new_module)
    return new_module

async def update_module(db: AsyncSession, module_id: int, name: str, icon: str, description: str, status: bool, updated_by: int):
    result = await db.execute(select(Module).filter(Module.id == module_id))
    module = result.scalars().first()
    if module:
        module.name = name
        module.icon = icon
        module.description = description
        module.status = status
        module.updated_by = updated_by
        await db.commit()
        await db.refresh(module)
    return module

async def delete_module(db: AsyncSession, module_id: int, updated_by: int):
    result = await db.execute(select(Module).filter(Module.id == module_id, Module.status == True))
    module = result.scalars().first()
    if module:
        module.status = False
        module.updated_by = updated_by
        await db.commit()
        await db.refresh(module)
    return module

async def assign_module_to_role(db: AsyncSession, role_id: int, module_id: int, created_by: int, updated_by: int):
    result = await db.execute(select(RoleModule).filter(RoleModule.role_id == role_id, RoleModule.module_id == module_id))
    exist_role_module = result.scalars().first()
    
    if exist_role_module:
        return exist_role_module  

    role_module = RoleModule(role_id=role_id, module_id=module_id, created_by=created_by, updated_by=updated_by)
    db.add(role_module)
    await db.commit()
    await db.refresh(role_module)
    return role_module

