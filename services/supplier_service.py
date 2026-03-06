def get_suppliers(part_number: str):

    part = part_number.upper()

    suppliers = [

        {
            "name": "Radwell",
            "url": f"https://www.radwell.com/en-US/Search/?q={part}"
        },

        {
            "name": "EU Automation",
            "url": f"https://www.euautomation.com/uk/search?q={part}"
        },

        {
            "name": "PLC Hardware",
            "url": f"https://www.plchardware.com/search?type=product&q={part}"
        },

        {
            "name": "MRO Electric",
            "url": f"https://www.mroelectric.com/search?q={part}"
        },

        {
            "name": "eBay",
            "url": f"https://www.ebay.com/sch/i.html?_nkw={part}"
        }

    ]

    return suppliers