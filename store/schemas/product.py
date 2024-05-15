from datetime import datetime
from typing import Optional
from pydantic import Field
from store.schemas.base import BaseSchemaMixIn, OutSchema


class ProductBase(BaseSchemaMixIn):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Quantity of the product")
    price: float = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixIn):
    ...


class ProductOut(ProductIn, OutSchema):
    ...


class ProductUpdate(BaseSchemaMixIn):
    quantity: Optional[int] = Field(None, description="Quantity of the product")
    price: Optional[float] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class ProductUpdateOut(ProductUpdate):
    ...
