from sqlalchemy import Column, Integer, String, Float
from database import Base


# =========================
# Products Table
# =========================

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    part_number = Column(String, unique=True, index=True)

    manufacturer = Column(String)

    quantity = Column(Integer, default=0)

    condition = Column(String)

    availability = Column(String)

    price = Column(Float)


# =========================
# Orders Table
# =========================

class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    part_number = Column(String)

    quantity = Column(Integer)

    customer = Column(String)

    status = Column(String)  # quotation / confirmed

    created_at = Column(String)