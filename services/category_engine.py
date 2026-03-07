def normalize_category(category):

    if not category:
        return "industrial-components"

    c = category.lower()

    if "plc" in c:
        return "plc-modules"

    if "hmi" in c:
        return "hmi-panels"

    if "contactor" in c:
        return "contactors"

    if "sensor" in c:
        return "sensors"

    if "relay" in c:
        return "relays"

    return c.replace(" ", "-")