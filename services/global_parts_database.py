# services/global_parts_database.py

def detect_global_industrial_brand(part):

    p = part.upper()

    brands = {

        # Siemens
        "6ES": "Siemens",
        "6AV": "Siemens",
        "3RT": "Siemens",
        "3RH": "Siemens",

        # Schneider
        "LC1D": "Schneider Electric",
        "XPS": "Schneider Electric",

        # Allen Bradley
        "1769": "Allen Bradley",
        "1756": "Allen Bradley",
        "1746": "Allen Bradley",

        # Omron
        "CJ": "Omron",
        "CP1": "Omron",
        "E2E": "Omron",

        # Mitsubishi
        "FX": "Mitsubishi",
        "QX": "Mitsubishi",

        # Yaskawa
        "SGDV": "Yaskawa",
        "SGDH": "Yaskawa",

        # Lenze
        "E82": "Lenze",

        # Turck
        "BI": "Turck",

        # Pepperl+Fuchs
        "NBB": "Pepperl+Fuchs",

        # Sick
        "WL": "Sick",
        "IME": "Sick",

        # Leuze
        "OG": "Leuze",

        # Datalogic
        "DT": "Datalogic",

        # Endress Hauser
        "PMC": "Endress+Hauser",

        # Vega
        "VEG": "Vega",

        # Rosemount
        "3051": "Rosemount",

        # Emerson
        "MTS": "Emerson",

        # Control Techniques
        "MD": "Control Techniques",

        # Eaton
        "DIL": "Eaton",

        # Wago
        "750": "Wago",

        # Phoenix Contact
        "290": "Phoenix Contact",

        # B&R
        "X20": "B&R",

        # Pilz
        "PNOZ": "Pilz",

        # LS
        "MC": "LS Electric",

        # Parker
        "PVP": "Parker",

        # Kollmorgen
        "AKM": "Kollmorgen",

        # Nidec
        "SK": "Nidec"

    }

    for prefix in brands:

        if p.startswith(prefix):

            return brands[prefix]

    return "Industrial"