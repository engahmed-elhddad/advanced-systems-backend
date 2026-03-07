# services/local_service.py

from database import SessionLocal
from models import Product


def normalize_part(part_number: str):

    if not part_number:
        return ""

    p = part_number.upper()

    p = p.replace(" ", "")
    p = p.replace("_", "-")

    return p


def search_local(part_number: str):

    db = SessionLocal()

    try:

        query = normalize_part(part_number)

        products = db.query(Product).all()

        results = []

        for product in products:

            p = normalize_part(product.part_number)

            if query in p or p in query:

                results.append({

                    "part_number": product.part_number,
                    "price": product.price,
                    "availability": product.availability,
                    "condition": product.condition,
                    "quantity": product.quantity

                })

        return results

    finally:

        db.close()