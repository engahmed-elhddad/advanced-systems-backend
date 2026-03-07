from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import random
from dotenv import load_dotenv

from database import engine, SessionLocal
from models import Base, Product

from services.local_service import search_local
from services.part_intelligence import detect_part_info
from services.datasheet_service import get_datasheet
from services.supplier_service import get_suppliers

from services.parts_graph import (
    get_related_parts,
    get_replacement_parts,
    get_accessories,
    get_compatible_modules,
)

from services.cross_reference_service import get_cross_reference
from services.ai_part_engine import analyze_part_number

from services.parts_index import generate_part_variants
from services.global_parts_engine import generate_part_family
from services.auto_discovery_engine import discover_similar_parts
from services.image_service import get_product_image

from services.brand_category_engine import detect_brand, detect_category
from services.industrial_ai_matching_engine import industrial_ai_matching

from services.part_normalizer import normalize_part_number
from services.industrial_part_parser import parse_industrial_part
from services.global_parts_index import generate_global_parts


# =========================
# API MODELS
# =========================

class RFQRequest(BaseModel):
    part_number: str
    quantity: int
    company: str
    email: str


# =========================
# ENV
# =========================

load_dotenv()
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


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
# MARKET SUPPLIERS
# =========================

def get_market_suppliers(part_number):

    suppliers = [
        "Radwell",
        "EU Automation",
        "Classic Automation"
    ]

    results = []

    for s in suppliers:
        results.append({
            "name": s,
            "price": random.randint(800,1200),
            "currency": "USD",
            "lead_time": "3-7 days"
        })

    return results


# =========================
# VIRTUAL PRODUCT
# =========================

def generate_virtual_product(part_number):

    p = normalize_part_number(part_number)

    parsed = parse_industrial_part(p) or {}

    brand = parsed.get("brand") or detect_brand(p)
    category = parsed.get("category") or detect_category(p)

    family = parsed.get("family")
    series = parsed.get("series")

    return {
        "part_number": p,
        "brand": brand,
        "category": category,
        "family": family,
        "series": series,
        "description": f"{p} industrial automation spare part used in industrial control systems",
    }


# =========================
# SMART SEARCH
# =========================

def smart_search(query, products):

    query = query.lower()
    results = []

    for p in products:

        part = p.part_number.lower()
        score = 0

        if part == query:
            score = 100

        elif part.startswith(query):
            score = 70

        elif query in part:
            score = 50

        if score > 0:

            results.append({
                "part_number": p.part_number,
                "score": score
            })

    return results


# =========================
# DISCOVER PARTS
# =========================

@app.get("/discover/{part_number}")
def discover_parts(part_number: str):

    part_number = normalize_part_number(part_number)

    variants = generate_part_variants(part_number)
    family = generate_part_family(part_number)
    discovered = discover_similar_parts(part_number)

    parts = list(set(
        [part_number] + variants + family + discovered
    ))

    return {
        "seed": part_number,
        "count": len(parts),
        "parts": parts[:500]
    }


# =========================
# SMART AI SEARCH
# =========================

@app.get("/smart-search")
def smart_industrial_search(query: str):

    query = normalize_part_number(query)

    brand = detect_brand(query)
    category = detect_category(query)

    ai_results = industrial_ai_matching(query)

    return {
        "query": query,
        "brand_detected": brand,
        "category_detected": category,
        "results": ai_results[:20]
    }


# =========================
# SEARCH ENGINE
# =========================

@app.get("/search")
def search(query: str):

    query = normalize_part_number(query)

    db = SessionLocal()

    try:

        products = db.query(Product).all()
        results = smart_search(query, products)

        variants = generate_part_variants(query)
        family = generate_part_family(query)
        discovered = discover_similar_parts(query)

        global_parts = generate_global_parts()

        expanded = variants + family + discovered + global_parts

        existing = {r["part_number"] for r in results}

        for part in expanded:

            if part not in existing:

                results.append({
                    "part_number": part,
                    "score": 40
                })

        results.sort(key=lambda x: x["score"], reverse=True)

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

    family = parsed.get("family")
    series = parsed.get("series")

    description = intelligence.get(
        "description",
        f"{part_number} industrial automation spare part"
    )

    datasheet = get_datasheet(part_number)
    suppliers = get_suppliers(part_number)
    market_suppliers = get_market_suppliers(part_number)

    results = search_local(part_number)

    related = get_related_parts(part_number)
    replacement = get_replacement_parts(part_number)
    accessories = get_accessories(part_number)
    compatible = get_compatible_modules(part_number)

    cross_reference = get_cross_reference(part_number)
    ai_matching = industrial_ai_matching(part_number)

    images = get_product_image(part_number)

    if results:

        product = results[0]

        return {

            "part_number": product["part_number"],
            "brand": brand,
            "category": category,
            "family": family,
            "series": series,

            "description": description,

            "images": images,
            "datasheet": datasheet,

            "suppliers": suppliers,
            "market_suppliers": market_suppliers,

            "related_parts": related,
            "replacement_parts": replacement,
            "accessories": accessories,
            "compatible_modules": compatible,
            "cross_reference": cross_reference,

            "ai_matching": ai_matching,

            "price": product.get("price"),
            "availability": product.get("availability"),
            "condition": product.get("condition"),
            "quantity": product.get("quantity"),

            "rfq_available": False
        }

    virtual = generate_virtual_product(part_number)

    return {

        **virtual,

        "images": images,
        "datasheet": datasheet,

        "suppliers": suppliers,
        "market_suppliers": market_suppliers,

        "related_parts": related,
        "replacement_parts": replacement,
        "accessories": accessories,
        "compatible_modules": compatible,
        "cross_reference": cross_reference,

        "ai_matching": ai_matching,

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
# INDUSTRIAL BRANDS
# =========================

BRANDS = [

"Siemens","Schneider Electric","Allen Bradley","ABB","Omron",
"Pilz","Endress+Hauser","Pepperl+Fuchs","Turck","Sick",
"IFM","Festo","SMC","Keyence","Mitsubishi",
"Vega","Beckhoff","Bosch Rexroth","Wago",
"Phoenix Contact","Lenze","Yokogawa","B&R Automation"

]


@app.get("/brands")
def get_brands():

    return {
        "count": len(BRANDS),
        "brands": BRANDS
    }


@app.get("/brand/{brand_name}")
def get_brand(brand_name: str):

    brand_name = brand_name.lower()

    return {

        "brand": brand_name,

        "description": f"{brand_name} industrial automation products supplier",

        "categories":[
            "PLC",
            "Drives",
            "Sensors",
            "Power Supplies",
            "Safety Systems",
            "HMI",
            "Industrial Networking"
        ],

        "top_products":[
            f"{brand_name} PLC",
            f"{brand_name} Drives",
            f"{brand_name} Sensors"
        ]

    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def home():

    return {
        "message": "Advanced Systems Backend Running 🚀"
    }