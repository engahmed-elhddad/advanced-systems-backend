def analyze_part(part_number: str):

    part = part_number.upper()

    result = {
        "brand": "Industrial",
        "category": "Component",
        "family": None
    }

    # Siemens PLC
    if part.startswith("6ES7"):

        result["brand"] = "Siemens"
        result["category"] = "PLC"
        result["family"] = "S7-300"

    # Siemens Contactors
    elif part.startswith("3RT"):

        result["brand"] = "Siemens"
        result["category"] = "Contactor"
        result["family"] = "SIRIUS"

    # Siemens Encoders
    elif part.startswith("6FX"):

        result["brand"] = "Siemens"
        result["category"] = "Encoder"

    # ABB Drives
    elif part.startswith("ACS"):

        result["brand"] = "ABB"
        result["category"] = "Drive"

    # Phoenix Contact
    elif part.startswith("PT"):

        result["brand"] = "Phoenix Contact"
        result["category"] = "Terminal Block"

    return result