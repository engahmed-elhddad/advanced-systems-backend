def search_nexar(part_number: str):
    """
    Manual Nexar search (Admin only)
    Replace later with real Nexar API call
    """

    # مؤقتًا لحد ما نربط Nexar فعليًا
    return [
        {
            "part_number": part_number,
            "price": 999.99,
            "availability": "External Supplier",
            "supplier": "Nexar Mock"
        }
    ]