from typing import Dict, Optional
import json
from datetime import datetime, timedelta
from app.models.cart import Cart, CartItem
from app.core.redis import redis_client
from app.config.settings import settings
import logging

logger = logging.getLogger("shopping.cart.api")


class CartService:
    def __init__(self):
        self.redis = redis_client
        self.prefix = settings.REDIS_PREFIX

    def _get_cart_key(self, user_id: str) -> str:
        return f"{self.prefix}{user_id}"

    def _serialize_cart(self, cart: Cart) -> str:
        return json.dumps({
            "user_id": cart.user_id,
            "items": [{
                "item": item.item,
                "quantity": item.quantity,
                "added_at": item.added_at.isoformat()
            } for item in cart.items]
        })

    def _deserialize_cart(self, user_id: str, data: Optional[str]) -> Optional[Cart]:
        if not data:
            return None

        cart_data = json.loads(data)
        items = [
            CartItem(
                item=item["item"],
                quantity=item["quantity"],
                added_at=datetime.fromisoformat(item["added_at"])
            )
            for item in cart_data["items"]
        ]
        return Cart(user_id=user_id, items=items)

    async def add_item(self, user_id: str, item: str, quantity: int) -> Cart:
        cart_key = self._get_cart_key(user_id)
        cart_data = self.redis.get(cart_key)

        if cart_data:
            cart = self._deserialize_cart(user_id, cart_data)
        else:
            cart = Cart(user_id=user_id)

        new_item = CartItem(
            item=item,
            quantity=quantity,
            added_at=datetime.utcnow()
        )
        cart.items.append(new_item)

        # Save to Redis with expiration
        self.redis.setex(
            cart_key,
            timedelta(hours=settings.CART_EXPIRY_HOURS),
            self._serialize_cart(cart)
        )

        return cart

    async def get_cart(self, user_id: str) -> Cart:
        cart_key = self._get_cart_key(user_id)
        cart_data = self.redis.get(cart_key)

        if not cart_data:
            raise KeyError(f"Cart not found for user {user_id}")

        cart = self._deserialize_cart(user_id, cart_data)
        return cart

    async def clear_cart(self, user_id: str) -> None:
        cart_key = self._get_cart_key(user_id)
        if not self.redis.exists(cart_key):
            raise KeyError(f"Cart not found for user {user_id}")

        self.redis.delete(cart_key)
