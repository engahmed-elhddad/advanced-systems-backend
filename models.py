from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


# =========================
# Products Table
# =========================

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    part_number = Column(String, unique=True, index=True)

    manufacturer = Column(String, index=True)

    quantity = Column(Integer, default=0)

    condition = Column(String)

    availability = Column(String)

    price = Column(Float)

    currency = Column(String, default="USD")

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)


# =========================
# Product Images Table
# =========================

class ProductImage(Base):

    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)

    part_number = Column(String, index=True)

    image_url = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# Orders Table
# =========================

class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    part_number = Column(String, index=True)

    quantity = Column(Integer)

    customer = Column(String)

    status = Column(String)  # quotation / confirmed

    created_at = Column(DateTime, default=datetime.utcnow)