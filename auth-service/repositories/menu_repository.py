from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from models.menu_model import Menu
from models.role_menu_model import RoleMenu
from sqlalchemy.orm import aliased

async def insert_role_menu(db: AsyncSession, role_id: int, menu_id: int):
    # Verificar si la relación ya existe
    result = await db.execute(
        select(RoleMenu).filter(
            RoleMenu.role_id == role_id,
            RoleMenu.menu_id == menu_id
        )
    )
    existing_relation = result.scalars().first()
    
    if existing_relation:
        return existing_relation  # Retornar la relación existente si ya existe

    # Crear una nueva relación
    new_relation = RoleMenu(role_id=role_id, menu_id=menu_id)
    db.add(new_relation)
    await db.commit()
    await db.refresh(new_relation)
    
    return new_relation

async def get_active_menus_flat_by_role(db: AsyncSession, role_id: int) -> List[Menu]:
    """Obtiene la lista plana de menús activos mediante CTE recursiva filtrados por el rol del JWT."""

    # 1. Caso base: Menús raíz activos del rol
    anchor = (
        select(Menu)
        .join(RoleMenu, RoleMenu.menu_id == Menu.id)  
        .where(
            and_(
                Menu.parent_id == None,
                Menu.status == True,
                RoleMenu.role_id == role_id      
            )
        )
        .cte(name="menu_tree_cte", recursive=True)
    )

    # 2. Caso recursivo: Hijos activos vinculados al rol
    recursive = (
        select(Menu)
        .join(anchor, Menu.parent_id == anchor.c.id)
        .join(RoleMenu, RoleMenu.menu_id == Menu.id)  
        .where(
            and_(
                Menu.status == True,          
                RoleMenu.role_id == role_id      
            )
        )
    )

    menu_cte = anchor.union_all(recursive)

    # Creamos un alias del modelo que apunta al CTE en lugar de la tabla física 'menus'
    menu_alias = aliased(Menu, menu_cte)

    # Consulta final usando el alias del CTE
    query = (
        select(menu_alias)
        .distinct()
    )
    
    result = await db.execute(query)
    return result.scalars().all()

async def get_all_menus(db: AsyncSession):
    result = await db.execute(
        select(Menu)
    )
    return result.scalars().all()
    

async def get_by_id(db: AsyncSession, menu_id: int) -> Menu | None:
    result = await db.execute(
        select(Menu)
        .options(
            selectinload(Menu.children).selectinload(Menu.children).selectinload(Menu.children)
        )
        .filter(Menu.id == menu_id)
    )
    return result.scalars().first()


async def get_descendant_ids(db: AsyncSession, menu_id: int) -> List[int]:
    """Obtiene los IDs de todos los descendientes usando CTE para validaciones o borrado en cascada."""
    anchor = (
        select(Menu.id)
        .where(Menu.id == menu_id)
        .cte(name="descendants_cte", recursive=True)
    )
    recursive = (
        select(Menu.id)
        .join(anchor, Menu.parent_id == anchor.c.id)
    )
    descendants_cte = anchor.union_all(recursive)
    result = await db.execute(select(descendants_cte.c.id))
    return result.scalars().all()


async def is_circular_reference(db: AsyncSession, menu_id: int, new_parent_id: Optional[int]) -> bool:
    """Verifica si asignar un nuevo parent_id genera un ciclo o bucle infinito."""
    if not new_parent_id:
        return False
    if menu_id == new_parent_id:
        return True
    
    descendants = await get_descendant_ids(db, menu_id)
    return new_parent_id in descendants


async def create(db: AsyncSession, data: dict) -> Menu:
    new_menu = Menu(**data)
    db.add(new_menu)
    await db.commit()
    await db.refresh(new_menu)
    
    result = await db.execute(
        select(Menu)
        .options(
            selectinload(Menu.children).selectinload(Menu.children).selectinload(Menu.children)
        )
        .filter(Menu.id == new_menu.id)
    )
    return result.scalars().first()


async def update(db: AsyncSession, menu: Menu, update_data: dict) -> Menu:
    for key, value in update_data.items():
        setattr(menu, key, value)
    await db.commit()
    await db.refresh(menu)
    
    result = await db.execute(
        select(Menu)
        .options(
            selectinload(Menu.children).selectinload(Menu.children).selectinload(Menu.children)
        )
        .filter(Menu.id == menu.id)
    )
    return result.scalars().first()


async def delete(db: AsyncSession, menu: Menu, updated_by: int) -> Menu:
    menu.status = False
    menu.updated_by = updated_by
    await db.commit()
    await db.refresh(menu)
    
    result = await db.execute(
        select(Menu)
        .options(
            selectinload(Menu.children).selectinload(Menu.children).selectinload(Menu.children)
        )
        .filter(Menu.id == menu.id)
    )
    return result.scalars().first()