from sqlalchemy import Column, Integer, String
from app.db import Base


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    ai_resolution = Column(String)