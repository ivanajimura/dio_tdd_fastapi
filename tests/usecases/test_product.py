from typing import List
import uuid

import pytest
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase

from tests.factories import product_data
from store.core.exceptions import NotFoundException


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == product_data()["name"]


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == product_data()["name"]


async def test_usecases_get_should_return_not_found():
    random_uid = uuid.uuid4()
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=random_uid)

    assert err.value.message == f"Product not found with filter UUID({random_uid})"


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_up, product_inserted):
    product_up.price = 7.500
    result = await product_usecase.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)
    assert result is True


async def test_usecases_delete_should_not_found():
    random_uid = uuid.uuid4()
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=random_uid)

    assert err.value.message == f"Product not found with filter UUID({random_uid})"
