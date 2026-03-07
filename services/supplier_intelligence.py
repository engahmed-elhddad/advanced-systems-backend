import random

def get_market_suppliers(part_number):

    suppliers = [

        {
            "name": "Radwell",
            "price": random.randint(800, 1200),
            "currency": "USD",
            "lead_time": "3-7 days"
        },

        {
            "name": "EU Automation",
            "price": random.randint(850, 1250),
            "currency": "USD",
            "lead_time": "5-10 days"
        },

        {
            "name": "Classic Automation",
            "price": random.randint(900, 1300),
            "currency": "USD",
            "lead_time": "4-8 days"
        }

    ]

    return suppliers