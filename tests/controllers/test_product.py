import uuid
from tests.factories import product_data
from fastapi import status
from typing import List
import pytest


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())
    assert response.status_code == status.HTTP_201_CREATED

    content = response.json()
    del content["created_at"]
    del content["updated_at"]
    del content["id"]
    assert content == {
        "name": "iPhone 14 Pro Max",
        "quantity": 10,
        "price": "8.499",
        "status": True,
    }


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")
    assert response.status_code == status.HTTP_200_OK

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert content == {
        "id": str(product_inserted.id),
        "name": "iPhone 14 Pro Max",
        "quantity": 10,
        "price": "8.499",
        "status": True,
    }


async def test_controller_get_should_return_not_found(
    client, products_url, product_inserted
):
    random_uid = uuid.uuid4()
    response = await client.get(f"{products_url}{random_uid}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Product not found with filter: {random_uid}"}


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )
    assert response.status_code == status.HTTP_200_OK
    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "7.500",
        "status": True,
    }


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    random_uid = uuid.uuid4()
    response = await client.delete(f"{products_url}{random_uid}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": f"Product not found with filter: {random_uid}"}
