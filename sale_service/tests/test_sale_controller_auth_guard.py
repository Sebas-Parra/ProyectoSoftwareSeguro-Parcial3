"""Zero Trust: sale_service no debe procesar ninguna operacion sin un
token valido firmado por el Master, sin importar si la base de datos
tendria o no la venta."""
import types

import pytest
from fastapi import HTTPException

from tests.db_helpers import run
from controllers import sale_controller
from dtos.sale_dto import SaleDTO


def _bad_credentials():
    return types.SimpleNamespace(credentials="esto-no-es-un-jwt-valido")


CASES = [
    ("create", lambda: sale_controller.create_sale_controller(
        None, SaleDTO(name="x", description="y", total=1.0, status=True), _bad_credentials()
    )),
    ("get_all", lambda: sale_controller.get_all_sales_controller(None, 1, 10, _bad_credentials())),
    ("update", lambda: sale_controller.update_sale_controller(
        None, 1, SaleDTO(name="x", description="y", total=1.0, status=True), _bad_credentials()
    )),
    ("delete", lambda: sale_controller.delete_sale_controller(None, 1, _bad_credentials())),
]


@pytest.mark.parametrize("name,call", CASES, ids=[c[0] for c in CASES])
def test_sale_controller_rejects_invalid_token(name, call):
    with pytest.raises(HTTPException) as exc_info:
        run(call())

    assert exc_info.value.status_code == 401
