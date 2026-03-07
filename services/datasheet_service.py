# services/datasheet_service.py

def normalize_part(part_number: str):

    if not part_number:
        return ""

    p = part_number.upper()

    p = p.replace(" ", "")
    p = p.replace("_", "-")

    return p


def get_datasheet(part_number: str):

    """
    Generate possible datasheet sources for industrial parts
    """

    p = normalize_part(part_number)

    datasheets = [

        # manufacturer search
        f"https://www.google.com/search?q={p}+datasheet",

        # RS Components
        f"https://www.rs-online.com/search/results/?query={p}",

        # Farnell / Element14
        f"https://www.element14.com/search?st={p}",

        # Mouser
        f"https://www.mouser.com/c/?q={p}",

        # DigiKey
        f"https://www.digikey.com/en/products/result?keywords={p}",

        # Radwell
        f"https://www.radwell.com/en-US/Buy/?term={p}"

    ]

    return datasheets