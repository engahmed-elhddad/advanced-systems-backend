# services/industrial_part_parser.py

from services.brand_category_engine import detect_brand, detect_category
from services.part_normalizer import normalize_part_number


def parse_industrial_part(part_number: str):

    p = normalize_part_number(part_number)

    brand = detect_brand(p)
    category = detect_category(p)

    family = None
    series = None
    part_type = None

    # Example logic based on structure (not fixed part numbers)

    if brand == "Siemens":

        if p.startswith("6ES7"):
            family = "SIMATIC"
            series = "S7"
            part_type = "PLC Module"

        elif p.startswith("6AV"):
            family = "SIMATIC"
            series = "HMI"
            part_type = "HMI Panel"

        elif p.startswith("3RT"):
            family = "SIRIUS"
            series = "Motor Control"
            part_type = "Contactor"

    if brand == "Allen Bradley":

        if p.startswith(("1756", "1769")):
            family = "ControlLogix"
            part_type = "PLC Controller"

    if brand == "Schneider Electric":

        if p.startswith("LC1"):
            family = "TeSys"
            part_type = "Contactor"

    if brand == "Omron":

        if p.startswith("E2E"):
            family = "Proximity Sensors"
            part_type = "Inductive Sensor"

    return {

        "part_number": p,
        "brand": brand,
        "category": category,
        "family": family,
        "series": series,
        "type": part_type

    }