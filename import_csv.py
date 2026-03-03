import csv
from database import SessionLocal
from models import Product

session = SessionLocal()

with open("stock.csv", newline="", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:

        raw_price = row["price"]

        if raw_price:
            clean_price = (
                raw_price
                .replace(",", "")
                .replace("\xa0", "")
                .strip()
            )
            price = float(clean_price)
        else:
            price = None

        product = Product(
            part_number=row["part_number"].strip(),
            price=price,
            availability=row["availability"].strip(),
            condition="Used"
        )

        session.merge(product)

    session.commit()

session.close()

print("✅ CSV Imported Successfully")