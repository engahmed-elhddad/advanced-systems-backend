# services/part_normalizer.py

import re


def normalize_part_number(part_number: str):

    if not part_number:
        return None

    p = part_number.upper()

    # remove spaces
    p = p.replace(" ", "")

    # replace slashes
    p = p.replace("/", "-")

    # remove strange characters
    p = re.sub(r"[^A-Z0-9\-]", "", p)

    return p