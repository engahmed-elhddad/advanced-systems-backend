# services/auto_discovery_engine.py

import re


def normalize_part(part_number: str):

    if not part_number:
        return ""

    p = part_number.upper()

    p = p.replace(" ", "")
    p = p.replace("_", "-")

    return p


def discover_similar_parts(part_number: str):

    """
    Generate possible similar parts based on structure
    """

    p = normalize_part(part_number)

    results = set()

    # split segments
    segments = re.split(r"[-/]", p)

    # progressively combine segments
    for i in range(len(segments)):

        part = "-".join(segments[: i + 1])

        if len(part) > 3:
            results.add(part)

    # remove separators
    results.add("".join(segments))

    # space version
    results.add(" ".join(segments))

    return list(results)