from sqlalchemy import Column, Integer, String
from app.db import Base

class Order(Base):
    __tablename__ = "orders"
    order_no = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    status = Column(String, nullable=False)

