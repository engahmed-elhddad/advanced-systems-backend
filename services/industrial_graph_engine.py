# services/industrial_graph_engine.py

def build_industrial_graph(part_number):

    p = part_number.upper()

    graph = {
        "compatible_modules": [],
        "replacement_parts": [],
        "accessories": [],
        "alternative_brands": []
    }

    # =========================
    # Siemens PLC
    # =========================

    if p.startswith("6ES7"):

        graph["compatible_modules"] = [

            "6ES7321-1BH02-0AA0",
            "6ES7322-1HF01-0AA0",
            "6ES7331-7KF02-0AB0",
            "6ES7332-5HF00-0AB0"

        ]

        graph["replacement_parts"] = [

            "6ES7314-6CG03-0AB0",
            "6ES7315-6FF04-0AB0"

        ]

        graph["accessories"] = [

            "6ES7972-0BB12-0XA0",
            "6ES7972-0BA52-0XA0"

        ]

        graph["alternative_brands"] = [

            {
                "brand": "Allen Bradley",
                "series": "ControlLogix"
            },

            {
                "brand": "Schneider",
                "series": "Modicon M340"
            }

        ]

    # =========================
    # Contactors
    # =========================

    if p.startswith(("3RT", "LC1D")):

        graph["replacement_parts"] = [

            "3RT1024-1BB40",
            "LC1D25"

        ]

        graph["accessories"] = [

            "3RH1921-1FA22",
            "LA1DN11"

        ]

        graph["alternative_brands"] = [

            {
                "brand": "Eaton",
                "series": "DILM"
            },

            {
                "brand": "ABB",
                "series": "AF Series"
            }

        ]

    # =========================
    # Sensors
    # =========================

    if p.startswith(("NBB", "BI", "OG", "DT")):

        graph["alternative_brands"] = [

            {
                "brand": "Sick",
                "series": "Inductive Sensors"
            },

            {
                "brand": "Turck",
                "series": "Proximity Sensors"
            }

        ]

    return graph