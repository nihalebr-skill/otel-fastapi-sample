from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime
from app.config.settings import settings


class CartItem(BaseModel):
    item: str
    quantity: int = Field(gt=0, le=settings.MAX_ITEM_QUANTITY,
                          description="Quantity must be greater than 0")
    added_at: datetime = Field(default_factory=datetime.utcnow)


class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []

    @validator('items')
    def validate_items_limit(cls, v):
        if len(v) > settings.MAX_CART_ITEMS:
            raise ValueError(
                f'Cart cannot contain more than {settings.MAX_CART_ITEMS} items')
        return v
