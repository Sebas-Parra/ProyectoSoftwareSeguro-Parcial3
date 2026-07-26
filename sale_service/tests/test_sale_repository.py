from tests.db_helpers import run, DbCase
from repositories import sale_repository


def test_insert_and_get_all_sales_paginates():
    async def scenario():
        async with DbCase() as db:
            for i in range(3):
                await sale_repository.insert_sale(db, f"Venta {i}", "desc", 10.0 + i, created_by=1, updated_by=1)

            page = await sale_repository.get_all_sales(db, page=1, limit=2)
            assert page["total"] == 3
            assert len(page["data"]) == 2
            assert page["total_pages"] == 2

    run(scenario())


def test_update_sale():
    async def scenario():
        async with DbCase() as db:
            sale = await sale_repository.insert_sale(db, "Venta 1", "desc", 10.0, created_by=1, updated_by=1)

            updated = await sale_repository.update_sale(db, sale.id, "Venta actualizada", "nueva desc", 20.0, updated_by=2)
            assert updated.name == "Venta actualizada"
            assert updated.total == 20.0

    run(scenario())


def test_update_sale_returns_none_when_not_found():
    async def scenario():
        async with DbCase() as db:
            result = await sale_repository.update_sale(db, 9999, "x", "y", 1.0, updated_by=1)
            assert result is None

    run(scenario())


def test_delete_sale_is_soft_delete():
    async def scenario():
        async with DbCase() as db:
            from sqlalchemy import select
            from models.sale_model import Sale

            sale = await sale_repository.insert_sale(db, "Venta 1", "desc", 10.0, created_by=1, updated_by=1)
            await sale_repository.delete_sale(db, sale.id, updated_by=1)

            result = await db.execute(select(Sale).filter(Sale.id == sale.id))
            still_there = result.scalars().first()
            assert still_there is not None
            assert still_there.status is False

    run(scenario())
