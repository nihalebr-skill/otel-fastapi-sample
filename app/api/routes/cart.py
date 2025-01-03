# app/api/routes/cart.py
from fastapi import APIRouter, Depends, HTTPException
from opentelemetry import trace
from app.services.cart_service import CartService
from app.api.dependencies import get_cart_service, record_cart_attributes
import logging

router = APIRouter()
tracer = trace.get_tracer(__name__)
logger = logging.getLogger("shopping.cart.api")


@router.post("/cart/{user_id}/items")
async def add_item(
    user_id: str,
    item: str,
    quantity: int,
    cart_service: CartService = Depends(get_cart_service)
):
    with tracer.start_as_current_span("add_item_to_cart") as span:
        try:
            logger.info(
                f"Adding {quantity} x {item} to cart for user {user_id}")
            cart = await cart_service.add_item(user_id, item, quantity)
            record_cart_attributes(user_id, "add_item", cart)(span)
            logger.info(f"Successfully added items to cart for user {user_id}")
            return {"status": "success", "cart": cart}
        except ValueError as e:
            span.record_exception(e)
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            span.record_exception(e)
            raise


@router.get("/cart/{user_id}")
async def get_cart(
    user_id: str,
    cart_service: CartService = Depends(get_cart_service)
):
    with tracer.start_as_current_span("get_cart") as span:
        try:
            logger.info(f"Retrieving cart for user {user_id}")
            cart = await cart_service.get_cart(user_id)
            record_cart_attributes(user_id, "get_cart", cart)(span)
            return {"cart": cart}
        except KeyError:
            logger.warning(f"Cart not found for user {user_id}")
            raise HTTPException(status_code=404, detail="Cart not found")
        except Exception as e:
            span.record_exception(e)
            raise


@router.delete("/cart/{user_id}")
async def clear_cart(
    user_id: str,
    cart_service: CartService = Depends(get_cart_service)
):
    with tracer.start_as_current_span("clear_cart") as span:
        try:
            logger.warning(f"Clearing cart for user {user_id}")
            cart = await cart_service.get_cart(user_id)
            record_cart_attributes(user_id, "clear_cart", cart)(span)
            await cart_service.clear_cart(user_id)
            return {"status": "success", "message": "Cart cleared"}
        except KeyError:
            logger.error(
                f"Attempted to clear non-existent cart for user {user_id}")
            raise HTTPException(status_code=404, detail="Cart not found")
        except Exception as e:
            span.record_exception(e)
            raise
