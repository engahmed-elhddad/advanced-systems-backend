from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from datetime import datetime

from database import engine, SessionLocal
from models import Base, Product, Order

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
# API Models
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


class StockUpdate(BaseModel):
    part_number: str
    change: int


class OrderRequest(BaseModel):
    part_number: str
    quantity: int
    customer: str


# =========================
# Add Product
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
# Update Stock
# =========================

@app.post("/update-stock")
def update_stock(data: StockUpdate):

    db = SessionLocal()

    product = db.query(Product).filter(Product.part_number == data.part_number).first()

    if not product:
        return {"error": "Product not found"}

    product.quantity += data.change

    if product.quantity < 0:
        product.quantity = 0

    db.commit()

    return {
        "part_number": product.part_number,
        "new_quantity": product.quantity
    }


# =========================
# Search
# =========================

@app.get("/search")
def search(part: str, page: int = 1, limit: int = 20):
    return engine_search(part)


# =========================
# Product Page
# =========================

@app.get("/product/{part_number}")
def get_product(part_number: str):

    intelligence = detect_part_info(part_number)

    datasheet = get_datasheet(part_number)

    suppliers = get_suppliers(part_number)

    results = search_local(part_number)

    image_url = f"https://static.radwell.com/images/products/{part_number}.jpg"

    if results:

        product = results[0]

        return {

            "part_number": product["part_number"],
            "brand": intelligence["manufacturer"],
            "category": intelligence["category"],
            "description": intelligence["description"],

            "title": f"{part_number} {intelligence['manufacturer']} Industrial Component",
            "seo_description": intelligence["description"],

            "datasheet": datasheet,
            "suppliers": suppliers,

            "image": image_url,

            "price": product["price"],
            "availability": product["availability"],
            "condition": product.get("condition") or "Used",
            "quantity": product.get("quantity", 0),

            "rfq_available": False
        }

    return {

        "part_number": part_number,
        "brand": intelligence["manufacturer"],
        "category": intelligence["category"],
        "description": intelligence["description"],

        "title": f"{part_number} {intelligence['manufacturer']} Industrial Component",
        "seo_description": intelligence["description"],

        "datasheet": datasheet,
        "suppliers": suppliers,

        "image": image_url,

        "price": None,
        "availability": "Not in Stock",
        "condition": None,
        "quantity": 0,

        "rfq_available": True
    }


# =========================
# Related Parts Engine
# =========================

@app.get("/related/{part_number}")
def related_parts(part_number: str):

    db = SessionLocal()

    try:

        prefix = part_number[:6]

        products = db.query(Product).filter(
            Product.part_number.like(f"{prefix}%")
        ).limit(6).all()

        return {
            "results": [
                {"part_number": p.part_number}
                for p in products
            ]
        }

    finally:

        db.close()


# =========================
# RFQ
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
# Create Quotation
# =========================

@app.post("/create-quotation")
def create_quotation(data: OrderRequest):

    db = SessionLocal()

    new_order = Order(

        part_number=data.part_number,
        quantity=data.quantity,
        customer=data.customer,
        status="quotation",
        created_at=str(datetime.now())

    )

    db.add(new_order)

    db.commit()

    return {

        "status": "Quotation Created"
    }


# =========================
# Confirm Order
# =========================

@app.post("/confirm-order/{order_id}")
def confirm_order(order_id: int):

    db = SessionLocal()

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        return {"error": "Order not found"}

    product = db.query(Product).filter(Product.part_number == order.part_number).first()

    if not product:
        return {"error": "Product not found in stock"}

    if product.quantity < order.quantity:
        return {"error": "Not enough stock"}

    product.quantity -= order.quantity

    order.status = "confirmed"

    db.commit()

    return {

        "status": "Order confirmed",
        "remaining_stock": product.quantity
    }


# =========================
# Nexar Admin Search
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
# All Products
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
# Sitemap
# =========================

@app.get("/sitemap.xml")
def sitemap():

    db = SessionLocal()

    products = db.query(Product).all()

    urls = ""

    for p in products:

        urls += f"""
        <url>
            <loc>https://advancedsystems-int.com/product/{p.part_number}</loc>
        </url>
        """

    xml = f"""
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {urls}
    </urlset>
    """

    return Response(content=xml, media_type="application/xml")


# =========================
# Health Check
# =========================

@app.get("/")
def home():
    return {"message": "Advanced Systems Backend Running 🚀"}