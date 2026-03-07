# services/global_parts_engine.py

import re


def extract_family_root(part_number: str):

    """
    Extract the base family of the part number.
    Example:
    6ES7315-2EH14-0AB0 → 6ES7315
    """

    if not part_number:
        return None

    p = part_number.upper()

    # split by separators
    parts = re.split(r"[-_/]", p)

    return parts[0]


def generate_part_family(part_number: str):

    """
    Generate family variants dynamically
    """

    family = []

    root = extract_family_root(part_number)

    if not root:
        return family

    family.append(root)

    # progressively shorten
    for i in range(len(root), 3, -1):

        variant = root[:i]

        if variant not in family:
            family.append(variant)

    return family