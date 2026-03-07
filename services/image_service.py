# services/image_service.py

def normalize_part(part_number: str):

    if not part_number:
        return ""

    p = part_number.upper()

    p = p.replace(" ", "")
    p = p.replace("_", "-")

    return p


def get_product_image(part_number: str):

    """
    Generate multiple industrial image sources
    """

    p = normalize_part(part_number)

    images = [

        # Radwell
        f"https://static.radwell.com/images/products/{p}.jpg",

        # RS Components
        f"https://media.rs-online.com/t_large/{p}.jpg",

        # Farnell / Element14
        f"https://www.element14.com/productimages/standard/en_GB/{p}.jpg",

        # Mouser
        f"https://www.mouser.com/images/{p}.jpg",

        # DigiKey
        f"https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/{p}.jpg",

        # fallback placeholder
        "/no-image.png"

    ]

    return images