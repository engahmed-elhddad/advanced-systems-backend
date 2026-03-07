def parse_query(query):

    q = query.lower()

    manufacturer = None
    category = None

    if "siemens" in q:
        manufacturer = "Siemens"

    if "plc" in q:
        category = "PLC"

    if "sensor" in q:
        category = "Sensor"

    if "contactor" in q:
        category = "Contactor"

    return {
        "manufacturer": manufacturer,
        "category": category
    }