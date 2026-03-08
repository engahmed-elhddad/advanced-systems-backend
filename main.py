from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import random
import csv
import io
import shutil
import zipfile
import tempfile

from dotenv import load_dotenv

from database import engine, SessionLocal
from models import Base, Product

from services.local_service import search_local
from services.part_intelligence import detect_part_info
from services.datasheet_service import get_datasheet
from services.parts_graph import (
    get_related_parts,
    get_replacement_parts,
)
from services.ai_part_engine import analyze_part_number
from services.image_service import get_product_image
from services.brand_category_engine import detect_brand, detect_category
from services.part_normalizer import normalize_part_number
from services.industrial_part_parser import parse_industrial_part


# =========================
# ENV
# =========================

load_dotenv()
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


# =========================
# ADMIN SECURITY
# =========================

def verify_admin(api_key: str = Header(None)):

    if api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")


# =========================
# API MODELS
# =========================

class RFQRequest(BaseModel):
    part_number: str
    quantity: int
    company: str
    email: str


# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="Advanced Systems API",
    version="1.0"
)

Base.metadata.create_all(bind=engine)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://advanced-systems-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# SEARCH ENGINE
# =========================

@app.get("/search")
def search(query: str):

    query = normalize_part_number(query)

    db = SessionLocal()

    try:

        products = db.query(Product).all()

        results = []

        for p in products:

            part = p.part_number.lower()

            if query in part:

                results.append({
                    "part_number": p.part_number
                })

        return {
            "query": query,
            "count": len(results),
            "results": results[:30]
        }

    finally:

        db.close()


# =========================
# PRODUCT PAGE
# =========================

@app.get("/product/{part_number}")
def get_product(part_number: str):

    part_number = normalize_part_number(part_number)

    parsed = parse_industrial_part(part_number) or {}

    intelligence = detect_part_info(part_number) or analyze_part_number(part_number) or {}

    brand = parsed.get("brand") or detect_brand(part_number)
    category = parsed.get("category") or detect_category(part_number)

    description = intelligence.get(
        "description",
        f"{part_number} industrial automation spare part"
    )

    datasheet = get_datasheet(part_number)

    results = search_local(part_number)

    related = get_related_parts(part_number)
    replacement = get_replacement_parts(part_number)

    images = get_product_image(part_number)

    if results:

        product = results[0]

        return {
            "part_number": product["part_number"],
            "brand": brand,
            "category": category,
            "description": description,
            "images": images,
            "datasheet": datasheet,
            "related_parts": related,
            "replacement_parts": replacement,
            "price": product.get("price"),
            "availability": product.get("availability"),
            "condition": product.get("condition"),
            "quantity": product.get("quantity"),
            "rfq_available": False
        }

    return {
        "part_number": part_number,
        "brand": brand,
        "category": category,
        "description": description,
        "images": images,
        "datasheet": datasheet,
        "related_parts": related,
        "replacement_parts": replacement,
        "availability": "Available on Request",
        "rfq_available": True
    }


# =========================
# AUTOCOMPLETE
# =========================

@app.get("/autocomplete")
def autocomplete(query: str):

    query = normalize_part_number(query)

    db = SessionLocal()

    try:

        products = db.query(Product).all()

        results = []

        for product in products:

            part = product.part_number.upper()

            if part.startswith(query):

                results.append({
                    "part_number": part
                })

        return {
            "query": query,
            "results": results[:10]
        }

    finally:

        db.close()


# =========================
# RFQ
# =========================

@app.post("/rfq")
def create_rfq(rfq: RFQRequest):

    part = normalize_part_number(rfq.part_number)

    return {
        "status": "RFQ received",
        "part_number": part,
        "quantity": rfq.quantity,
        "company": rfq.company,
        "email": rfq.email
    }


# =========================
# ADMIN PRODUCT LIST
# =========================

@app.get("/admin/products")
def admin_products(api_key: str = Header(None)):

    verify_admin(api_key)

    db = SessionLocal()

    try:

        products = db.query(Product).limit(200).all()

        results = []

        for p in products:

            results.append({
                "part_number": p.part_number,
                "price": p.price,
                "quantity": p.quantity,
                "condition": p.condition,
                "availability": p.availability
            })

        return {
            "count": len(results),
            "products": results
        }

    finally:

        db.close()


# =========================
# ADMIN UPDATE PRODUCT
# =========================

@app.put("/admin/update-product")
def update_product(data: dict, api_key: str = Header(None)):

    verify_admin(api_key)

    db = SessionLocal()

    part = normalize_part_number(data["part_number"])

    product = db.query(Product).filter(
        Product.part_number == part
    ).first()

    if not product:

        return {"error": "not found"}

    product.price = data.get("price")
    product.quantity = data.get("quantity")
    product.condition = data.get("condition")
    product.availability = data.get("availability")

    db.commit()

    return {"status": "updated"}


# =========================
# ADMIN DELETE PRODUCT
# =========================

@app.delete("/admin/delete-product/{part_number}")
def delete_product(part_number: str, api_key: str = Header(None)):

    verify_admin(api_key)

    db = SessionLocal()

    part = normalize_part_number(part_number)

    product = db.query(Product).filter(
        Product.part_number == part
    ).first()

    if product:

        db.delete(product)
        db.commit()

    return {"status": "deleted"}


# =========================
# ADMIN IMPORT SYSTEM
# =========================

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/admin/import-products")
async def import_products(file: UploadFile = File(...), api_key: str = Header(None)):

    verify_admin(api_key)

    db = SessionLocal()

    content = await file.read()

    csv_file = io.StringIO(content.decode("utf-8"))

    reader = csv.DictReader(csv_file)

    count = 0

    for row in reader:

        part = normalize_part_number(row["part_number"])

        price = float(row.get("price") or 0)
        quantity = int(row.get("quantity") or 0)

        existing = db.query(Product).filter(
            Product.part_number == part
        ).first()

        if existing:

            existing.price = price
            existing.availability = row.get("availability")
            existing.condition = row.get("condition")
            existing.quantity = quantity

        else:

            product = Product(
                part_number=part,
                price=price,
                availability=row.get("availability"),
                condition=row.get("condition"),
                quantity=quantity
            )

            db.add(product)

        count += 1

    db.commit()

    return {
        "status": "success",
        "imported": count
    }


@app.post("/admin/upload-image")
async def upload_image(file: UploadFile = File(...), api_key: str = Header(None)):

    verify_admin(api_key)

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "uploaded",
        "filename": file.filename
    }


@app.post("/admin/bulk-import")
async def bulk_import(file: UploadFile = File(...), api_key: str = Header(None)):

    verify_admin(api_key)

    db = SessionLocal()

    temp_dir = tempfile.mkdtemp()

    zip_path = os.path.join(temp_dir, file.filename)

    with open(zip_path, "wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        zip_ref.extractall(temp_dir)

    csv_path = os.path.join(temp_dir, "products.csv")

    count = 0

    if os.path.exists(csv_path):

        with open(csv_path, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                part = normalize_part_number(row["part_number"])

                price = float(row.get("price") or 0)
                quantity = int(row.get("quantity") or 0)

                product = Product(
                    part_number=part,
                    price=price,
                    availability=row.get("availability"),
                    condition=row.get("condition"),
                    quantity=quantity
                )

                db.add(product)

                count += 1

    db.commit()

    return {
        "status": "bulk import completed",
        "products_imported": count
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def home():

    return {
        "message": "Advanced Systems Backend Running 🚀"
    }