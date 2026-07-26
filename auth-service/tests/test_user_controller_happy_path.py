from tests.db_helpers import run, DbCase
from tests.auth_test_helpers import make_admin_context, bearer
from controllers import user_controller


def test_admin_can_register_list_get_update_and_delete_user():
    async def scenario():
        async with DbCase() as db:
            admin, role, access_token, _ = await make_admin_context(db)
            creds = bearer(access_token)

            register_response = await user_controller.register_user_controller(
                db, "vendedor1", "Pass1234!", creds
            )
            assert register_response["message"] == "Usuario registrado exitosamente"

            listing = await user_controller.get_all_users_controller(db, 1, 10, creds)
            assert listing["total"] == 2  # admin + vendedor1

            new_user = next(u for u in listing["data"] if u["username"] == "vendedor1")

            fetched = await user_controller.get_user_by_id_controller(db, new_user["id"], creds)
            assert fetched["username"] == "vendedor1"

            update_response = await user_controller.update_user_controller(
                db, new_user["id"], "vendedor1_actualizado", "NuevaPass1!", creds
            )
            assert update_response["message"] == "Usuario actualizado exitosamente"

            delete_response = await user_controller.delete_user_controller(db, new_user["id"], creds)
            assert delete_response["message"] == "Usuario eliminado exitosamente"

    run(scenario())
