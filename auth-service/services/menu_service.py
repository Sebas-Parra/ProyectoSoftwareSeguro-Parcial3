from sqlalchemy.ext.asyncio import AsyncSession
from repositories import menu_repository
from typing import List, Any
from fastapi import HTTPException

async def get_active_menus_flat_service(db: AsyncSession, role_id: int) -> List[Any]:
    print(f"Fetching active menus for role_id: {role_id}")
    # 1. Obtenemos la lista plana desde el repositorio usando la CTE con el rol
    menus = await menu_repository.get_active_menus_flat_by_role(db, role_id)
    
    # 2. Transformamos y armamos la jerarquía limpia para evitar duplicados en la raíz
    return _build_menu_tree(menus)

def _build_menu_tree(menus: list) -> list:
    """
    Construye un árbol jerárquico limpio omitiendo elementos inactivos (status == False).
    """
    menu_map = {}
    
    # Filtrar estrictamente solo los que tengan status True por seguridad adicional
    active_menus = [menu for menu in menus if getattr(menu, "status", True) is True]

    # Mapear únicamente los menús activos
    for menu in active_menus:
        menu_map[menu.id] = {
            "id": menu.id,
            "nombre": menu.nombre,
            "url": menu.url,
            "modulo_id": menu.modulo_id,
            "parent_id": menu.parent_id,
            "status": menu.status,
            "children": []
        }

    tree = []
    
    # Organizar la jerarquía asegurando que no se cuelen inactivos
    for menu in active_menus:
        if menu.parent_id is not None:
            # Si el padre existe en el mapa y está activo
            if menu.parent_id in menu_map:
                menu_map[menu.parent_id]["children"].append(menu_map[menu.id])
        else:
            # Menús raíz
            tree.append(menu_map[menu.id])
            
    return tree

async def get_by_id_service(db: AsyncSession, menu_id: int):
    return await menu_repository.get_by_id(db, menu_id)

async def get_descendant_ids_service(db: AsyncSession, menu_id: int) -> List[int]:
    return await menu_repository.get_descendant_ids(db, menu_id)

async def create_menu_service(db: AsyncSession, data: dict, created_by: int) -> Any:
    menu_data = {**data, "created_by": created_by, "updated_by": created_by}
    return await menu_repository.create(db, menu_data)

async def update_menu_service(db: AsyncSession, menu_id: int, update_data: dict, updated_by: int):
    menu = await menu_repository.get_by_id(db, menu_id)
    if not menu:
        return None
    
    # Validar que el nuevo parent_id no genere un bucle infinito
    new_parent_id = update_data.get("parent_id")
    if new_parent_id is not None:
        is_cyclic = await menu_repository.is_circular_reference(db, menu_id, new_parent_id)
        if is_cyclic:
            raise HTTPException(
                status_code=400, 
                detail="Referencia cíclica detectada: Un menú no puede ser hijo de sí mismo ni de sus descendientes."
            )

    filtered_data = {k: v for k, v in update_data.items() if v is not None}
    filtered_data["updated_by"] = updated_by
    return await menu_repository.update(db, menu, filtered_data)

async def delete_menu_service(db: AsyncSession, menu_id: int, updated_by: int):
    menu = await menu_repository.get_by_id(db, menu_id)
    if not menu:
        return None
    return await menu_repository.delete(db, menu, updated_by)

async def insert_role_menu_service(db: AsyncSession, role_id: int, menu_id: int, created_by: int = None):
    return await menu_repository.insert_role_menu(db, role_id, menu_id, created_by=created_by, updated_by=created_by)



async def get_all_menus_service(db: AsyncSession):
    """
    Obtiene todos los menús, incluyendo los inactivos, y construye un árbol jerárquico.
    """
    return await menu_repository.get_all_menus(db)