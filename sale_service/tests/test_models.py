from models.sale_model import Sale


def test_sale_model_instantiation():
    sale = Sale(name="Venta 1", description="una venta", total=99.5)
    assert sale.name == "Venta 1"
    assert sale.total == 99.5
