# models.py

from sqlalchemy import Column, String, Float
from database import Base


class Product(Base):
    __tablename__ = "products"

    part_number = Column(String, primary_key=True, index=True)
    price = Column(Float)
    availability = Column(String)
    condition = Column(String, default="Used")   # 👈 ضيف دي