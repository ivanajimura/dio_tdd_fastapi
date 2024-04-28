from pydantic import Field
from store.schemas.base import BaseSchemaMixIn


class ProductIn(BaseSchemaMixIn):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Quantity of the product")
    price: float = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")
