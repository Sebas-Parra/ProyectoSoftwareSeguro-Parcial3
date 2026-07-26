from tests.db_helpers import run, DbCase
from tests.auth_test_helpers import bearer
from repositories import role_repository, user_repository
from services import user_service
from controllers import auth_controller
from dtos.auth_dto import LoginDTO, SelectRoleDTO


async def _seed_admin(db):
    role = await role_repository.insert_role(db, "administrador", "rol admin", "pi-crown", None, None)
    hashed = user_service._hash_password("Vikingofarifor123.")
    user = await user_repository.insert_user(db, "administrador", hashed, None, None)
    await role_repository.asign_role_to_user(db, user.id, role.id, None, None)
    return user, role


def test_login_controller_returns_temp_token_and_roles():
    async def scenario():
        async with DbCase() as db:
            await _seed_admin(db)

            response = await auth_controller.login_controller(
                db, LoginDTO(username="administrador", password="Vikingofarifor123.")
            )

            assert "temp_token" in response
            assert response["roles"][0]["name"] == "administrador"

    run(scenario())


def test_full_login_select_role_refresh_logout_flow():
    async def scenario():
        async with DbCase() as db:
            await _seed_admin(db)

            login_response = await auth_controller.login_controller(
                db, LoginDTO(username="administrador", password="Vikingofarifor123.")
            )
            temp_token = login_response["temp_token"]

            select_response = await auth_controller.select_role_controller(
                db, SelectRoleDTO(role_id=1), bearer(temp_token)
            )
            assert "access_token" in select_response
            assert "refresh_token" in select_response

            refresh_response = await auth_controller.refresh_token_controller(
                bearer(select_response["refresh_token"])
            )
            assert "access_token" in refresh_response

            logout_response = await auth_controller.logout_controller(
                bearer(refresh_response["access_token"])
            )
            assert logout_response["message"] == "Sesión cerrada exitosamente"

    run(scenario())
