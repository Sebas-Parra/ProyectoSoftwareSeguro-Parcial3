import time
import types

import jwt as pyjwt

from tests.db_helpers import run, DbCase
from controllers import sale_controller
from dtos.sale_dto import SaleDTO


def _valid_token(master_private_key, user_id=1):
    now = int(time.time())
    payload = {
        "sub": str(user_id), "username": "vendedor", "role": "vendedor", "role_id": 5,
        "type": "access", "exp": now + 900, "iat": now,
    }
    token = pyjwt.encode(payload, master_private_key, algorithm="RS256")
    return types.SimpleNamespace(credentials=token)


def test_authenticated_user_can_crud_sales(master_private_key):
    async def scenario():
        async with DbCase() as db:
            creds = _valid_token(master_private_key)

            created = await sale_controller.create_sale_controller(
                db, SaleDTO(name="Venta 1", description="desc", total=100.0, status=True), creds
            )
            assert created.id is not None

            listing = await sale_controller.get_all_sales_controller(db, 1, 10, creds)
            assert listing["total"] == 1

            updated = await sale_controller.update_sale_controller(
                db, created.id, SaleDTO(name="Venta actualizada", description="desc2", total=200.0, status=True), creds
            )
            assert updated.name == "Venta actualizada"

            delete_response = await sale_controller.delete_sale_controller(db, created.id, creds)
            assert delete_response["message"] == "Venta eliminada exitosamente"

    run(scenario())


def test_update_sale_controller_returns_404_for_missing_sale(master_private_key):
    from fastapi import HTTPException
    import pytest

    async def scenario():
        async with DbCase() as db:
            creds = _valid_token(master_private_key)
            with pytest.raises(HTTPException) as exc_info:
                await sale_controller.update_sale_controller(
                    db, 9999, SaleDTO(name="x", description="y", total=1.0, status=True), creds
                )
            assert exc_info.value.status_code == 404

    run(scenario())
