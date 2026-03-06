def detect_part_info(part):

    part = part.upper()

    if part.startswith("6ES7"):
        return {
            "manufacturer": "Siemens",
            "category": "PLC Module"
        }

    if part.startswith("3RT"):
        return {
            "manufacturer": "Siemens",
            "category": "Contactor"
        }

    if part.startswith("NBB"):
        return {
            "manufacturer": "Pepperl+Fuchs",
            "category": "Proximity Sensor"
        }

    if part.startswith("FX"):
        return {
            "manufacturer": "Mitsubishi",
            "category": "PLC"
        }

    return {
        "manufacturer": "Unknown",
        "category": "Industrial Automation Component"
    }


def search_nexar(part_number: str):
    """
    Simulated Nexar external supplier search
    """

    intelligence = detect_part_info(part_number)

    return [
        {
            "part_number": part_number,
            "manufacturer": intelligence["manufacturer"],
            "category": intelligence["category"],
            "price": 999.99,
            "availability": "External Supplier",
            "supplier": "External Distributor"
        }
    ]