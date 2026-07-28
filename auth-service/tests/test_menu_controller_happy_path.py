from tests.db_helpers import run, DbCase
from tests.auth_test_helpers import make_admin_context, bearer
from controllers import menu_controller
from repositories import module_repository
from dtos.menu_dto import MenuCreateDTO, MenuUpdateDTO


def test_admin_can_manage_menus_and_see_own_tree():
    async def scenario():
        async with DbCase() as db:
            admin, admin_role, access_token, _ = await make_admin_context(db)
            creds = bearer(access_token)

            module = await module_repository.insert_module(db, "Administración", "pi-shield", "desc", None, None)

            root = await menu_controller.create_menu_controller(
                db, MenuCreateDTO(nombre="Administración", url=None, modulo_id=module.id, parent_id=None), creds
            )
            child = await menu_controller.create_menu_controller(
                db, MenuCreateDTO(nombre="Ventas", url="/home/sales", modulo_id=module.id, parent_id=root.id), creds
            )

            await menu_controller.insert_role_menu_controller(db, admin_role.id, root.id, creds)
            await menu_controller.insert_role_menu_controller(db, admin_role.id, child.id, creds)

            tree = await menu_controller.get_active_menus_flat_controller(db, creds)
            assert len(tree) == 1
            assert tree[0]["children"][0]["nombre"] == "Ventas"

            all_menus = await menu_controller.get_all_menus_controller(db, creds)
            assert len(all_menus) == 2

            updated = await menu_controller.update_menu_controller(
                db, child.id, MenuUpdateDTO(nombre="Ventas Online"), creds
            )
            assert updated.nombre == "Ventas Online"

            delete_response = await menu_controller.delete_menu_controller(db, child.id, creds)
            assert delete_response["message"] == "Menú eliminado exitosamente"

    run(scenario())
