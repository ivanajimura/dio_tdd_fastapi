from pydantic import ValidationError
import pytest
from store.schemas.product import ProductIn
from tests.factories import product_data


def test_schemas_return_success():
    data = product_data()
    product = ProductIn.model_validate(
        data
    )  # equivalent to: product = ProductIn.(**data)

    assert product.name == data["name"]


def test_schemas_return_raise():
    data = {"name": "iPhone 14 Pro Max", "quantity": 10, "price": "8.499"}
    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "iPhone 14 Pro Max", "quantity": 10, "price": "8.499"},
        "url": "https://errors.pydantic.dev/2.7/v/missing",
    }
