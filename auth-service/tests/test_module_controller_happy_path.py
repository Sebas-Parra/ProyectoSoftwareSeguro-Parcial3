from tests.db_helpers import run, DbCase
from tests.auth_test_helpers import make_admin_context, bearer
from controllers import module_controller
from dtos.module_dto import ModuleDTO


def test_admin_can_manage_modules_and_assign_to_role():
    async def scenario():
        async with DbCase() as db:
            admin, admin_role, access_token, _ = await make_admin_context(db)
            creds = bearer(access_token)

            module = await module_controller.insert_module_controller(
                db, ModuleDTO(name="Ventas", description="modulo de ventas", icon="pi-cart", status=True), creds
            )

            modules = await module_controller.get_all_modules_controller(db, creds)
            assert len(modules) == 1

            update_response = await module_controller.update_module_controller(
                db, module.id,
                ModuleDTO(name="Ventas Online", description="desc", icon="pi-globe", status=True),
                creds,
            )
            assert update_response["message"] == "Módulo actualizado exitosamente"

            assign_response = await module_controller.assign_module_to_role_controller(
                db, admin_role.id, module.id, creds
            )
            assert assign_response.role_id == admin_role.id
            assert assign_response.module_id == module.id

            delete_response = await module_controller.delete_module_controller(db, module.id, creds)
            assert delete_response["message"] == "Módulo eliminado exitosamente"

    run(scenario())
