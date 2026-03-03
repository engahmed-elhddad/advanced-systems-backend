from database import SessionLocal
from models import Product


def search_local(part_number: str):
    session = SessionLocal()

    results = session.query(Product).filter(
        Product.part_number.ilike(f"%{part_number}%")
    ).all()

    session.close()

    return [
        {
            "part_number": p.part_number,
            "price": p.price,
            "availability": p.availability,
            "condition": p.condition   # 🔥 دي كانت ناقصة
        }
        for p in results
    ]