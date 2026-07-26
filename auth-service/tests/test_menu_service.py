import pytest
from fastapi import HTTPException

from tests.db_helpers import run, DbCase
from tests.test_menu_repository import _seed_menu_tree
from services import menu_service


def test_get_active_menus_flat_service_builds_nested_tree():
    async def scenario():
        async with DbCase() as db:
            role, root, child = await _seed_menu_tree(db)

            tree = await menu_service.get_active_menus_flat_service(db, role.id)

            assert len(tree) == 1
            assert tree[0]["id"] == root.id
            assert len(tree[0]["children"]) == 1
            assert tree[0]["children"][0]["id"] == child.id

    run(scenario())


def test_update_menu_service_rejects_circular_reference():
    async def scenario():
        async with DbCase() as db:
            role, root, child = await _seed_menu_tree(db)

            with pytest.raises(HTTPException) as exc_info:
                await menu_service.update_menu_service(
                    db, root.id, {"parent_id": child.id}, updated_by=1
                )

            assert exc_info.value.status_code == 400

    run(scenario())


def test_update_menu_service_updates_allowed_fields():
    async def scenario():
        async with DbCase() as db:
            role, root, child = await _seed_menu_tree(db)

            updated = await menu_service.update_menu_service(
                db, child.id, {"nombre": "Ventas Online"}, updated_by=1
            )

            assert updated.nombre == "Ventas Online"

    run(scenario())


def test_delete_menu_service_returns_none_for_missing_menu():
    async def scenario():
        async with DbCase() as db:
            result = await menu_service.delete_menu_service(db, 9999, updated_by=1)
            assert result is None

    run(scenario())
