# services/industrial_ai_matching_engine.py

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

    """
    Extract industrial series from part number
    Example:
    6ES7315-2EH14-0AB0 → 6ES7315
    """

    p = normalize_part(part_number)

    segments = re.split(r"[-/]", p)

    return segments[0]


def industrial_ai_matching(part_number: str):

    """
    Generate intelligent industrial matches
    """

    p = normalize_part(part_number)

    brand = detect_brand(p)

    category = detect_category(p)

    series = extract_series(p)

    matches = []

    # Similar series suggestion
    matches.append({
        "type": "series_match",
        "series": series
    })

    # Same category suggestion
    matches.append({
        "type": "category_match",
        "category": category
    })

    # Cross brand suggestion
    matches.append({
        "type": "cross_brand",
        "original_brand": brand,
        "target_category": category
    })

    return matches