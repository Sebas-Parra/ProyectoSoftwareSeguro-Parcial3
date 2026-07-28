from tests.db_helpers import run, DbCase
from tests.auth_test_helpers import make_admin_context, bearer
from controllers import role_controller, user_controller
from dtos.role_dto import RoleDTO


def test_admin_can_manage_roles_and_assign_them_to_users():
    async def scenario():
        async with DbCase() as db:
            admin, admin_role, access_token, _ = await make_admin_context(db)
            creds = bearer(access_token)

            insert_response = await role_controller.insert_role_controller(
                db, RoleDTO(name="vendedor", description="rol de ventas", icon="pi-user", status=True), creds
            )
            new_role = insert_response["role"]

            roles = await role_controller.get_all_roles_controller(db, creds)
            assert len(roles) == 2

            update_response = await role_controller.update_role_controller(
                db, new_role.id,
                RoleDTO(name="vendedor senior", description="desc", icon="pi-star", status=True),
                creds,
            )
            assert update_response["message"] == "Rol actualizado exitosamente"

            await user_controller.register_user_controller(db, "vendedor1", "Pass1234!", creds)
            listing = await user_controller.get_all_users_controller(db, 1, 10, creds)
            target_user = next(u for u in listing["data"] if u["username"] == "vendedor1")

            assign_response = await role_controller.asign_role_to_user_controller(
                db, target_user["id"], new_role.id, creds
            )
            assert assign_response["message"] == "Rol asignado al usuario exitosamente"

            unassign_response = await role_controller.desasign_role_from_user_controller(
                db, target_user["id"], new_role.id, creds
            )
            assert unassign_response["message"] == "Rol desasignado del usuario exitosamente"

            delete_response = await role_controller.delete_role_controller(db, new_role.id, creds)
            assert delete_response["message"] == "Rol eliminado exitosamente"

    run(scenario())
