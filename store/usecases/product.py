from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.core.exceptions import NotFoundException
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())
        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})
        if not result:
            raise NotFoundException(message=f"Product not found with filter UUID({id})")
        return ProductOut(**result)

    async def query(
        self,
        quantity_min=None,
        quantity_max=None,
        price_min=None,
        price_max=None,
        name_partial=None,
        status=None,
    ) -> List[ProductOut]:
        filter_query = {}
        if quantity_min:
            if "quantity" not in filter_query.keys():
                filter_query["quantity"] = {}
            filter_query["quantity"]["$gte"] = quantity_min
        if quantity_max:
            if "quantity" not in filter_query.keys():
                filter_query["quantity"] = {}
            filter_query["quantity"]["$lte"] = quantity_max
        if price_min:
            if "price" not in filter_query.keys():
                filter_query["price"] = {}
            filter_query["price"]["$gte"] = price_min
        if price_max:
            if "price" not in filter_query.keys():
                filter_query["price"] = {}
            filter_query["price"]["$lte"] = price_max
        if name_partial:
            filter_query["name"] = {"$regex": f"{name_partial}"}
        if status is not None:
            filter_query["status"] = status
        return [
            ProductOut(**item)
            async for item in self.collection.find(filter=filter_query)
        ]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        if not result:
            raise NotFoundException(message=f"Product not found with filter UUID({id})")
        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter UUID({id})")
        result = await self.collection.delete_one({"id": id})
        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
