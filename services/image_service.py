def get_product_image(part_number: str):

    part = part_number.upper()

    sources = [

        f"https://static.radwell.com/images/products/{part}.jpg",

        f"https://media.rs-online.com/t_large/F{part}.jpg",

        f"https://www.euautomation.com/images/products/{part}.jpg"

    ]

    return sources[0]