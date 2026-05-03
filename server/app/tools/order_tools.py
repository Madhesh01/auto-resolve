from app.db import AsyncSessionLocal
from app.models.order import Order
from app.models.ticket import Ticket
from sqlalchemy import select
from sqlalchemy.exc import DBAPIError

async def get_order_status(order_no: int) -> dict:
    """ Gets the current order status against a given order number """
    try: 
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Order.status).where(Order.order_no==order_no))
            order = result.scalar_one_or_none()

            if not order:
                return {"error": True, "message": f"Status not found for order {order_no}"}
            
            return {"error": False, "message": f"Order status : {order}"}
    
    except Exception as e:
        return {"error": True, "message": f"Error : {str(e)}"}



async def cancel_order(order_no: int) -> dict:
    """Cancels an order. Only call this if get_order_status confirms the order is PLACED, CONFIRMED, or SHIPPED — not if it is already DELIVERED, CANCELLED, or REFUNDED."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Order).where(Order.order_no==order_no))
            order = result.scalar_one_or_none()

            if not order:
                return {"error": True, "message": f"Order {order_no} not found"}
            
            order.status = "cancelled"
            await session.commit()
            return {"error": False, "message": f"Order {order_no} has been cancelled."}
    
    except DBAPIError:
        return {"error":True, "message": "Invalid input"}
    
    except Exception as e:
        return {"error": True, "message": f"Error : {str(e)}"}
        


async def update_shipping_address(order_no: int, new_address:str) -> dict:
    """Updates the shipping address. Only call this if get_order_status confirms the order is PLACED or CONFIRMED — address cannot be changed once the order is SHIPPED or later."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Order).where(Order.order_no==order_no))
            order = result.scalar_one_or_none()

            if not order:
                return {"error": True, "message": f"Order {order_no} not found."}

            order.address = new_address
            await session.commit()
            return {"error": False, "message":f"Shipping address of order {order_no} has been updated to {new_address}"}

    except Exception as e:
        return {"error": True, "message": f"Error : {str(e)}"}


async def request_refund(order_no: int) -> dict:
    """Processes a refund. Only call this if get_order_status confirms the order is DELIVERED or CANCELLED."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Order).where(Order.order_no == order_no))
            order = result.scalar_one_or_none()

            if not order:
                return {"error": True, "message": f"Order {order_no} not found."}

            if order.price is None:
                return {"error": True, "message": f"Refund could not be processed — price not available for order {order_no}."}

            order.status = "REFUNDED"
            await session.commit()
            return {"error": False, "message": f"Refund of ₹{order.price} processed for order {order_no}."}

    except Exception as e:
        return {"error": True, "message": f"Error: {str(e)}"}


async def escalate_to_human(order_no: int, reason: str) -> dict:
    """Escalates a ticket to a human agent when the issue cannot be resolved automatically"""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Order).where(Order.order_no == order_no))
            order = result.scalar_one_or_none() 

            if not order:
                return {"error": True, "message": f"Order {order_no} not found."}

            order.status = "ESCALATED"
            await session.commit()
            return {"error": False, "message": f"Order {order_no} has been escalated to a human agent. Reason: {reason}"}

    except Exception as e:
        return {"error": True, "message": f"Error: {str(e)}"}


async def report_damaged_item(order_no: int, description: str) -> dict:
    """Reports a damaged or missing item. Only call this if get_order_status confirms the order is DELIVERED or OUT_FOR_DELIVERY — do not call this for orders that are PLACED, CONFIRMED, or SHIPPED."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Order).where(Order.order_no == order_no))
            order = result.scalar_one_or_none()

            if not order:
                return {"error": True, "message": f"Order {order_no} not found."}

            order.status = "DAMAGED"
            await session.commit()
            return {"error": False, "message": f"Damage report filed for order {order_no}: {description}"}

    except Exception as e:
        return {"error": True, "message": f"Error: {str(e)}"}


TOOLS = [get_order_status, cancel_order, update_shipping_address, request_refund, escalate_to_human, report_damaged_item]
