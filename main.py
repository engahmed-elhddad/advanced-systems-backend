from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from database import engine, SessionLocal
from models import Base, Product
from search_engine import search_part as engine_search
from services.local_service import search_local
from services.nexar_service import search_nexar
from services.part_intelligence import detect_part_info
from services.datasheet_service import get_datasheet
from services.supplier_service import get_suppliers


# =========================
# Load ENV
# =========================
load_dotenv()
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


# =========================
# App
# =========================
app = FastAPI(title="Advanced Systems API")


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://advanced-systems-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Create tables
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# Models for API
# =========================
class ProductCreate(BaseModel):
    part_number: str
    manufacturer: str | None = None
    condition: str | None = "Used"
    availability: str | None = "In Stock"
    price: float | None = 0
    quantity: int | None = 0


class RFQRequest(BaseModel):
    part_number: str
    quantity: int
    company: str
    email: str


# =========================
# Add Product (Stock Manager)
# =========================
@app.post("/add-product")
def add_product(product: ProductCreate):

    db = SessionLocal()

    try:
        new_product = Product(
            part_number=product.part_number,
            price=product.price,
            availability=product.availability,
            condition=product.condition,
            quantity=product.quantity
        )

        db.add(new_product)
        db.commit()

        return {"status": "Product Added"}

    finally:
        db.close()


# =========================
# Public Search
# =========================
@app.get("/search")
def search(part: str, page: int = 1, limit: int = 20):
    return engine_search(part)


# =========================
# Product Page Endpoint
# =========================
@app.get("/product/{part_number}")
def get_product(part_number: str):

    intelligence = detect_part_info(part_number)
    datasheet = get_datasheet(part_number)
    suppliers = get_suppliers(part_number)

    results = search_local(part_number)

    if results:
        product = results[0]

        return {
            "part_number": product["part_number"],
            "manufacturer": intelligence["manufacturer"],
            "category": intelligence["category"],
            "description": intelligence["description"],
            "datasheet": datasheet,
            "suppliers": suppliers,
            "price": product["price"],
            "availability": product["availability"],
            "condition": product.get("condition") or "Used",
            "quantity": product.get("quantity", 0),
            "rfq_available": False
        }

    return {
        "part_number": part_number,
        "manufacturer": intelligence["manufacturer"],
        "category": intelligence["category"],
        "description": intelligence["description"],
        "datasheet": datasheet,
        "suppliers": suppliers,
        "price": None,
        "availability": "Not in Stock",
        "condition": None,
        "quantity": 0,
        "rfq_available": True
    }


# =========================
# RFQ Endpoint
# =========================
@app.post("/rfq")
def create_rfq(rfq: RFQRequest):

    return {
        "status": "RFQ received",
        "part_number": rfq.part_number,
        "quantity": rfq.quantity,
        "company": rfq.company,
        "email": rfq.email
    }


# =========================
# Admin Manual Nexar Search
# =========================
@app.get("/admin/nexar-search")
def admin_nexar_search(part: str, x_api_key: str = Header(None)):

    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    results = search_nexar(part)

    return {
        "source": "Nexar (Manual Admin)",
        "count": len(results),
        "results": results
    }


# =========================
# All Products (For Sitemap)
# =========================
@app.get("/all-products")
def all_products():

    db = SessionLocal()

    try:
        products = db.query(Product).all()

        results = [
            {"part_number": p.part_number}
            for p in products
        ]

        return {
            "count": len(results),
            "results": results
        }

    finally:
        db.close()


# =========================
# Health Check
# =========================
@app.get("/")
def home():
    return {"message": "Advanced Systems Backend Running 🚀"}