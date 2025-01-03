# app/api/dependencies.py
from fastapi import Request
from opentelemetry import trace
from typing import Callable
from app.models.cart import Cart
from app.services.cart_service import CartService


def get_cart_service() -> CartService:
    return CartService()


def record_cart_attributes(user_id: str, action: str, cart: Cart) -> Callable:
    def record(span: trace.Span):
        span.set_attribute("shopping.cart.size", len(cart.items))
        span.set_attribute("shopping.cart.action", action)
        span.set_attribute("user.id", user_id)
    return record
