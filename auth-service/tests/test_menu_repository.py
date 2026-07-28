from tests.db_helpers import run, DbCase
from repositories import menu_repository, role_repository


async def _seed_menu_tree(db):
    """Crea: Administracion (raiz) -> Ventas (hijo), y un rol con permiso
    sobre ambos niveles (igual que exige la CTE: cada nivel necesita su
    propia fila en role_menus)."""
    role = await role_repository.insert_role(db, "vendedor", "rol de ventas", "pi-user", None, None)

    root = await menu_repository.create(db, {
        "nombre": "Administración", "url": None, "modulo_id": 1, "parent_id": None,
        "created_by": 1, "updated_by": 1,
    })
    child = await menu_repository.create(db, {
        "nombre": "Ventas", "url": "/home/sales", "modulo_id": 1, "parent_id": root.id,
        "created_by": 1, "updated_by": 1,
    })

    await menu_repository.insert_role_menu(db, role.id, root.id)
    await menu_repository.insert_role_menu(db, role.id, child.id)

    return role, root, child


def test_cte_returns_full_branch_when_role_has_all_levels():
    async def scenario():
        async with DbCase() as db:
            role, root, child = await _seed_menu_tree(db)

            menus = await menu_repository.get_active_menus_flat_by_role(db, role.id)
            menu_ids = {m.id for m in menus}

            assert menu_ids == {root.id, child.id}

    run(scenario())


def test_cte_excludes_children_when_parent_not_assigned_to_role():
    """Aunque el rol tenga permiso sobre el hijo, si NO tiene el padre
    asignado, la CTE no debe devolver el hijo (asi esta implementada:
    cada nivel debe estar explicitamente en role_menus)."""
    async def scenario():
        async with DbCase() as db:
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)
            root = await menu_repository.create(db, {
                "nombre": "Administración", "url": None, "modulo_id": 1, "parent_id": None,
                "created_by": 1, "updated_by": 1,
            })
            child = await menu_repository.create(db, {
                "nombre": "Ventas", "url": "/home/sales", "modulo_id": 1, "parent_id": root.id,
                "created_by": 1, "updated_by": 1,
            })

            # Solo se asigna el hijo, NO el padre
            await menu_repository.insert_role_menu(db, role.id, child.id)

            menus = await menu_repository.get_active_menus_flat_by_role(db, role.id)
            assert menus == []

    run(scenario())


def test_cte_excludes_menus_of_other_roles():
    async def scenario():
        async with DbCase() as db:
            role_a, root_a, child_a = await _seed_menu_tree(db)
            role_b = await role_repository.insert_role(db, "otro_rol", "desc", "pi-user", None, None)

            menus_b = await menu_repository.get_active_menus_flat_by_role(db, role_b.id)
            assert menus_b == []

    run(scenario())


def test_cte_excludes_inactive_menus():
    async def scenario():
        async with DbCase() as db:
            role, root, child = await _seed_menu_tree(db)

            await menu_repository.delete(db, child, updated_by=1)  # soft delete

            menus = await menu_repository.get_active_menus_flat_by_role(db, role.id)
            menu_ids = {m.id for m in menus}
            assert menu_ids == {root.id}

    run(scenario())


def test_insert_role_menu_sets_audit_fields():
    async def scenario():
        async with DbCase() as db:
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)
            menu = await menu_repository.create(db, {
                "nombre": "Ventas", "url": "/home/sales", "modulo_id": 1, "parent_id": None,
                "created_by": 1, "updated_by": 1,
            })

            relation = await menu_repository.insert_role_menu(db, role.id, menu.id, created_by=1, updated_by=1)

            assert relation.created_by == 1
            assert relation.updated_by == 1
            assert relation.status is True

    run(scenario())


def test_insert_role_menu_is_idempotent_and_keeps_original_audit():
    async def scenario():
        async with DbCase() as db:
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)
            menu = await menu_repository.create(db, {
                "nombre": "Ventas", "url": "/home/sales", "modulo_id": 1, "parent_id": None,
                "created_by": 1, "updated_by": 1,
            })

            first = await menu_repository.insert_role_menu(db, role.id, menu.id, created_by=1, updated_by=1)
            second = await menu_repository.insert_role_menu(db, role.id, menu.id, created_by=2, updated_by=2)

            assert first.created_by == second.created_by == 1

    run(scenario())


def test_is_circular_reference_detects_self_and_descendant():
    async def scenario():
        async with DbCase() as db:
            role, root, child = await _seed_menu_tree(db)

            assert await menu_repository.is_circular_reference(db, root.id, root.id) is True
            assert await menu_repository.is_circular_reference(db, root.id, child.id) is True
            assert await menu_repository.is_circular_reference(db, child.id, root.id) is False
            assert await menu_repository.is_circular_reference(db, root.id, None) is False

    run(scenario())


def test_get_descendant_ids():
    async def scenario():
        async with DbCase() as db:
            role, root, child = await _seed_menu_tree(db)

            descendants = await menu_repository.get_descendant_ids(db, root.id)
            assert set(descendants) == {root.id, child.id}

    run(scenario())
