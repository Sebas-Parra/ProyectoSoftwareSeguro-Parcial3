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


def test_get_module_names_by_role_returns_only_assigned_active_modules():
    async def scenario():
        async with DbCase() as db:
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)
            ventas = await module_repository.insert_module(db, "Ventas", "pi-cart", "desc", None, None)
            rrhh = await module_repository.insert_module(db, "RRHH", "pi-users", "desc", None, None)

            await module_repository.assign_module_to_role(db, role.id, ventas.id, None, None)

            names = await module_repository.get_module_names_by_role(db, role.id)
            assert names == ["Ventas"]

            # Un modulo no asignado a este rol no debe aparecer
            other_role = await role_repository.insert_role(db, "rrhh_manager", "desc", "pi-user", None, None)
            await module_repository.assign_module_to_role(db, other_role.id, rrhh.id, None, None)
            assert await module_repository.get_module_names_by_role(db, role.id) == ["Ventas"]

    run(scenario())


def test_get_module_names_by_role_excludes_inactive_modules():
    async def scenario():
        async with DbCase() as db:
            role = await role_repository.insert_role(db, "vendedor", "desc", "pi-user", None, None)
            ventas = await module_repository.insert_module(db, "Ventas", "pi-cart", "desc", None, None)
            await module_repository.assign_module_to_role(db, role.id, ventas.id, None, None)

            await module_repository.delete_module(db, ventas.id, updated_by=1)

            assert await module_repository.get_module_names_by_role(db, role.id) == []

    run(scenario())
