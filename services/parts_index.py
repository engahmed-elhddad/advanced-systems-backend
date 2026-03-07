# services/parts_index.py

import re


def normalize_part(part_number: str):

    if not part_number:
        return ""

    p = part_number.upper()

    # remove spaces
    p = p.replace(" ", "")

    return p


def split_part_segments(part_number: str):

    """
    Split part number into segments using '-' or other separators
    """

    return re.split(r"[-_/]", part_number)


def generate_part_variants(part_number: str):

    p = normalize_part(part_number)

    variants = set()

    variants.add(p)

    # split segments
    segments = split_part_segments(p)

    # progressive build
    current = ""

    for seg in segments:

        if current:
            current = current + "-" + seg
        else:
            current = seg

        variants.add(current)

    # remove separators version
    variants.add("".join(segments))

    # space separated version
    variants.add(" ".join(segments))

    return list(variants)