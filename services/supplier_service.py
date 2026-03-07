# services/supplier_service.py

def normalize_part(part_number: str):

    if not part_number:
        return ""

    p = part_number.upper()

    p = p.replace(" ", "")
    p = p.replace("_", "-")

    return p


def get_suppliers(part_number: str):

    """
    Generate supplier search links for industrial parts
    """

    p = normalize_part(part_number)

    suppliers = [

        {
            "name": "Radwell",
            "url": f"https://www.radwell.com/en-US/Buy/?term={p}"
        },

        {
            "name": "EU Automation",
            "url": f"https://www.euautomation.com/search/?q={p}"
        },

        {
            "name": "Classic Automation",
            "url": f"https://www.classicautomation.com/search/?q={p}"
        },

        {
            "name": "MRO Electric",
            "url": f"https://www.mroelectric.com/search?q={p}"
        },

        {
            "name": "PLC Hardware",
            "url": f"https://www.plchardware.com/search?q={p}"
        },

        {
            "name": "RS Components",
            "url": f"https://www.rs-online.com/search/results/?query={p}"
        },

        {
            "name": "Farnell",
            "url": f"https://www.element14.com/search?st={p}"
        },

        {
            "name": "Mouser",
            "url": f"https://www.mouser.com/c/?q={p}"
        },

        {
            "name": "DigiKey",
            "url": f"https://www.digikey.com/en/products/result?keywords={p}"
        }

    ]

    return suppliers