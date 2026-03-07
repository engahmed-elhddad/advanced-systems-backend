# services/cross_reference_service.py

from services.brand_category_engine import detect_brand, detect_category


def get_cross_reference(part_number: str):

    if not part_number:
        return []

    brand = detect_brand(part_number)

    category = detect_category(part_number)

    # all supported industrial brands
    industrial_brands = [

        "SIEMENS",
        "ALLEN BRADLEY",
        "SCHNEIDER ELECTRIC",
        "ABB",
        "OMRON",
        "YASKAWA",
        "EATON",
        "PHOENIX CONTACT",
        "WAGO",
        "TURCK",
        "SICK",
        "LEUZE",
        "PEPPERL+FUCHS",
        "VEGA",
        "ENDRESS+HAUSER",
        "PARKER",
        "LENZE",
        "CONTROL TECHNIQUES",
        "KOLLMORGEN",
        "NIDEC"

    ]

    alternatives = []

    for b in industrial_brands:

        if b != brand:

            alternatives.append({

                "type": "cross_brand",

                "original_brand": brand,

                "alternative_brand": b,

                "category": category

            })

    return alternatives