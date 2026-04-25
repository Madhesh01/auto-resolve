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
    """ Cancels a order against a given order number """
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
    """ Updates the shipping address of a order against a order no and updates it to the new address"""
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


TOOLS = [get_order_status, cancel_order, update_shipping_address]
