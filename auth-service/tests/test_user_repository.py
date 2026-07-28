import pytest

from tests.db_helpers import run, DbCase
from repositories import user_repository


def test_insert_and_get_user_by_name():
    async def scenario():
        async with DbCase() as db:
            user = await user_repository.insert_user(db, "juan", "hashed-pass", None, None)
            assert user.id is not None

            fetched = await user_repository.get_user_by_name(db, "juan")
            assert fetched is not None
            assert fetched.username == "juan"

    run(scenario())


def test_insert_user_rejects_duplicate_username():
    async def scenario():
        async with DbCase() as db:
            await user_repository.insert_user(db, "juan", "hashed-pass", None, None)
            with pytest.raises(ValueError):
                await user_repository.insert_user(db, "juan", "otra-clave", None, None)

    run(scenario())


def test_get_user_by_id_excludes_inactive_users():
    async def scenario():
        async with DbCase() as db:
            user = await user_repository.insert_user(db, "juan", "hashed-pass", None, None)
            await user_repository.delete_user(db, user.id, updated_by=1)

            fetched = await user_repository.get_user_by_id(db, user.id)
            assert fetched is None  # soft-deleted -> no debe aparecer

    run(scenario())


def test_delete_user_is_soft_delete():
    async def scenario():
        async with DbCase() as db:
            user = await user_repository.insert_user(db, "juan", "hashed-pass", None, None)
            await user_repository.delete_user(db, user.id, updated_by=1)

            # El registro sigue existiendo fisicamente, solo status=False
            from sqlalchemy import select
            from models.user_model import User
            result = await db.execute(select(User).filter(User.id == user.id))
            still_there = result.scalars().first()
            assert still_there is not None
            assert still_there.status is False

    run(scenario())


def test_update_user_rejects_username_taken_by_another_user():
    async def scenario():
        async with DbCase() as db:
            await user_repository.insert_user(db, "juan", "hash1", None, None)
            maria = await user_repository.insert_user(db, "maria", "hash2", None, None)

            with pytest.raises(ValueError):
                await user_repository.update_user(db, maria.id, "juan", "hash2", updated_by=1)

    run(scenario())


def test_get_all_users_paginates_and_hides_password():
    async def scenario():
        async with DbCase() as db:
            for i in range(3):
                await user_repository.insert_user(db, f"user{i}", "hash", None, None)

            page = await user_repository.get_all_users(db, page=1, limit=2)
            assert page["total"] == 3
            assert len(page["data"]) == 2
            assert "password" not in page["data"][0]

    run(scenario())


def test_get_all_users_excludes_soft_deleted():
    async def scenario():
        async with DbCase() as db:
            activo = await user_repository.insert_user(db, "activo", "hash", None, None)
            inactivo = await user_repository.insert_user(db, "inactivo", "hash", None, None)
            await user_repository.delete_user(db, inactivo.id, updated_by=1)

            page = await user_repository.get_all_users(db, page=1, limit=10)

            assert page["total"] == 1
            assert [u["id"] for u in page["data"]] == [activo.id]

    run(scenario())


def test_get_user_roles_returns_only_active_roles():
    async def scenario():
        async with DbCase() as db:
            from repositories import role_repository
            user = await user_repository.insert_user(db, "juan", "hash", None, None)
            role = await role_repository.insert_role(db, "vendedor", "rol de ventas", "pi-user", None, None)
            await role_repository.asign_role_to_user(db, user.id, role.id, None, None)

            roles = await user_repository.get_user_roles(db, user.id)
            assert len(roles) == 1
            assert roles[0]["name"] == "vendedor"

            await role_repository.delete_role(db, role.id, updated_by=1)
            roles_after_delete = await user_repository.get_user_roles(db, user.id)
            assert roles_after_delete == []

    run(scenario())
