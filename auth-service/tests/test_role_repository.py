from tests.db_helpers import run, DbCase
from repositories import role_repository, user_repository


def test_insert_and_list_roles():
    async def scenario():
        async with DbCase() as db:
            await role_repository.insert_role(db, "vendedor", "rol de ventas", "pi-user", None, None)
            roles = await role_repository.get_all_roles(db)
            assert len(roles) == 1
            assert roles[0].name == "vendedor"

    run(scenario())


def test_update_role():
    async def scenario():
        async with DbCase() as db:
            role = await role_repository.insert_role(db, "vendedor", "desc vieja", "pi-user", None, None)
            updated = await role_repository.update_role(
                db, role.id, "vendedor senior", "pi-star", "desc nueva", True, updated_by=1
            )
            assert updated.name == "vendedor senior"
            assert updated.description == "desc nueva"

    run(scenario())


def test_delete_role_is_soft_delete_and_ignores_already_deleted():
    async def scenario():
        async with DbCase() as db:
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)

            deleted = await role_repository.delete_role(db, role.id, updated_by=1)
            assert deleted.status is False

            # Volver a "eliminar" un rol ya inactivo no debe romper ni reactivarlo
            deleted_again = await role_repository.delete_role(db, role.id, updated_by=1)
            assert deleted_again is None

    run(scenario())


def test_asign_and_desasign_role_to_user():
    async def scenario():
        async with DbCase() as db:
            user = await user_repository.insert_user(db, "juan", "hash", None, None)
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)

            await role_repository.asign_role_to_user(db, user.id, role.id, None, None)
            roles = await user_repository.get_user_roles(db, user.id)
            assert len(roles) == 1

            removed = await role_repository.desasign_role_from_user(db, user.id, role.id)
            assert removed is True

            # Verificamos directamente la tabla pivote en lugar de reusar
            # get_user_roles (que usa joinedload y cachea la coleccion en el
            # mismo User ya cargado en esta sesion; en la app real cada
            # request usa una sesion nueva).
            from sqlalchemy import select
            from models.user_roles_model import UserRole
            result = await db.execute(
                select(UserRole).filter(UserRole.user_id == user.id, UserRole.role_id == role.id)
            )
            assert result.scalars().first() is None

    run(scenario())


def test_asign_role_to_user_is_idempotent():
    async def scenario():
        async with DbCase() as db:
            user = await user_repository.insert_user(db, "juan", "hash", None, None)
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)

            first = await role_repository.asign_role_to_user(db, user.id, role.id, None, None)
            second = await role_repository.asign_role_to_user(db, user.id, role.id, None, None)
            assert first.user_id == second.user_id
            assert first.role_id == second.role_id

    run(scenario())
