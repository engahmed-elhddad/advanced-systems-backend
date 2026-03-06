from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from database import engine
from models import Base, Product
from database import SessionLocal
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
# 🔥 PART INTELLIGENCE
# =========================

# =========================
# 🔥 DATASHEET ENGINE
# =========================
def guess_datasheet(part, manufacturer):

    part = part.upper()

    if manufacturer == "Siemens":
        return f"https://www.google.com/search?q={part}+siemens+datasheet+pdf"

    if manufacturer == "Pepperl+Fuchs":
        return f"https://www.google.com/search?q={part}+pepperl+fuchs+datasheet+pdf"

    if manufacturer == "Mitsubishi":
        return f"https://www.google.com/search?q={part}+mitsubishi+datasheet+pdf"

    return f"https://www.google.com/search?q={part}+datasheet+pdf"


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
            "suppliers":suppliers,
            "price": product["price"],
            "availability": product["availability"],
            "condition": product.get("condition") or "Used",
            "rfq_available": False
        }

    return {
        "part_number": part_number,
        "manufacturer": intelligence["manufacturer"],
        "category": intelligence["category"],
        "description": intelligence["description"],
        "datasheet": datasheet,
        "suppliers":suppliers,
        "price": None,
        "availability": "Not in Stock",
        "condition": None,
        "rfq_available": True
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
# Health Check
# =========================
@app.get("/")
def home():
    return {"message": "Advanced Systems Backend Running 🚀"}


# =========================
# All Products (For Sitemap)
# =========================
@app.get("/all-products")
def all_products():

    db = SessionLocal()

    products = db.query(Product).all()

    results = [
        {"part_number": p.part_number}
        for p in products
    ]

    return {
        "count": len(results),
        "results": results
    }