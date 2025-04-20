from ninja import Schema
from typing import Optional


class UserOut(Schema):
    id: int
    username: str
    role: str


class ProductOut(Schema):
    id: int
    name: str
    description: str
    price: float


class ProductFilter(Schema):
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    search:   Optional[str]   = None
