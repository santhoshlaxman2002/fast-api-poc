from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)
    in_stock: bool