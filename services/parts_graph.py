# services/parts_graph.py

import re


def normalize_part(part_number: str):

    if not part_number:
        return ""

    p = part_number.upper()

    p = p.replace(" ", "")
    p = p.replace("_", "-")

    return p


def extract_series(part_number: str):

    """
    Extract the main industrial series
    Example:
    6ES7315-2EH14-0AB0 → 6ES7315
    """

    p = normalize_part(part_number)

    segments = re.split(r"[-/]", p)

    return segments[0]


# =========================
# RELATED PARTS
# =========================

def get_related_parts(part_number: str):

    series = extract_series(part_number)

    return [
        {
            "type": "series_related",
            "series": series
        }
    ]


# =========================
# REPLACEMENTS
# =========================

def get_replacement_parts(part_number: str):

    series = extract_series(part_number)

    return [
        {
            "type": "replacement_candidate",
            "series": series
        }
    ]


# =========================
# ACCESSORIES
# =========================

def get_accessories(part_number: str):

    series = extract_series(part_number)

    return [
        {
            "type": "possible_accessory",
            "series": series
        }
    ]


# =========================
# COMPATIBLE MODULES
# =========================

def get_compatible_modules(part_number: str):

    series = extract_series(part_number)

    return [
        {
            "type": "compatible_module",
            "series": series
        }
    ]