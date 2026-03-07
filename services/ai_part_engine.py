# services/ai_part_engine.py

import re

from services.brand_category_engine import detect_brand, detect_category


def normalize_part(part_number: str):

    if not part_number:
        return ""

    p = part_number.upper()

    p = p.replace(" ", "")
    p = p.replace("_", "-")

    return p


def extract_series(part_number: str):

    p = normalize_part(part_number)

    segments = re.split(r"[-/]", p)

    return segments[0]


def detect_structure(part_number: str):

    """
    Analyze structure of part number
    """

    p = normalize_part(part_number)

    letters = sum(c.isalpha() for c in p)

    numbers = sum(c.isdigit() for c in p)

    length = len(p)

    return {

        "letters": letters,
        "numbers": numbers,
        "length": length

    }


def analyze_part_number(part_number: str):

    """
    Universal industrial part analyzer
    """

    if not part_number:
        return None

    p = normalize_part(part_number)

    brand = detect_brand(p)

    category = detect_category(p)

    series = extract_series(p)

    structure = detect_structure(p)

    description = f"{brand} {category} industrial automation component"

    return {

        "manufacturer": brand,

        "category": category,

        "series": series,

        "structure": structure,

        "description": description

    }