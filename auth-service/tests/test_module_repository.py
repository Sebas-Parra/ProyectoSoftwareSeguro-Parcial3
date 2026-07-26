from tests.db_helpers import run, DbCase
from repositories import module_repository, role_repository


def test_insert_and_list_modules():
    async def scenario():
        async with DbCase() as db:
            await module_repository.insert_module(db, "Ventas", "pi-cart", "modulo de ventas", None, None)
            modules = await module_repository.get_all_modules(db)
            assert len(modules) == 1
            assert modules[0].name == "Ventas"

    run(scenario())


def test_update_module():
    async def scenario():
        async with DbCase() as db:
            module = await module_repository.insert_module(db, "Ventas", "pi-cart", "desc", None, None)
            updated = await module_repository.update_module(
                db, module.id, "Ventas Online", "pi-globe", "desc nueva", True, updated_by=1
            )
            assert updated.name == "Ventas Online"

    run(scenario())


def test_delete_module_is_soft_delete():
    async def scenario():
        async with DbCase() as db:
            module = await module_repository.insert_module(db, "Ventas", "pi-cart", "desc", None, None)
            deleted = await module_repository.delete_module(db, module.id, updated_by=1)
            assert deleted.status is False

    run(scenario())


def test_assign_module_to_role_is_idempotent():
    async def scenario():
        async with DbCase() as db:
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)
            module = await module_repository.insert_module(db, "Ventas", "pi-cart", "desc", None, None)

            first = await module_repository.assign_module_to_role(db, role.id, module.id, None, None)
            second = await module_repository.assign_module_to_role(db, role.id, module.id, None, None)
            assert first.role_id == second.role_id
            assert first.module_id == second.module_id

    run(scenario())
