import csv
import os
import shutil

from database import SessionLocal
from models import Product

# مسارات
CSV_FILE = "stock.csv"
IMAGES_SOURCE = "images"  # فولدر الصور اللي هتحط فيه الصور قبل الاستيراد
FRONTEND_PRODUCTS_DIR = "../advanced_systems_frontend/public/products"

db = SessionLocal()

def copy_images(part_number):
    """
    ينقل كل الصور الخاصة بالقطعة:
    PART.jpg
    PART-1.jpg
    PART-2.jpg
    ...
    """
    if not os.path.exists(IMAGES_SOURCE):
        return

    for file in os.listdir(IMAGES_SOURCE):

        name, ext = os.path.splitext(file)

        if ext.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue

        if name.upper().startswith(part_number):

            src = os.path.join(IMAGES_SOURCE, file)
            dst = os.path.join(FRONTEND_PRODUCTS_DIR, file)

            os.makedirs(FRONTEND_PRODUCTS_DIR, exist_ok=True)
            shutil.copy(src, dst)


with open(CSV_FILE, newline="", encoding="utf-8") as f:

    reader = csv.DictReader(f)

    for row in reader:

        part = row["part_number"].strip().upper()

        existing = db.query(Product).filter(
            Product.part_number == part
        ).first()

        if existing:

            existing.price = row.get("price")
            existing.availability = row.get("availability")
            existing.condition = row.get("condition")
            existing.quantity = row.get("quantity")

        else:

            product = Product(
                part_number=part,
                price=row.get("price"),
                availability=row.get("availability"),
                condition=row.get("condition"),
                quantity=row.get("quantity")
            )

            db.add(product)

        copy_images(part)

db.commit()

print("Import Completed ✅")