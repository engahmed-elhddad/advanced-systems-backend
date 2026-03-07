# services/brand_category_engine.py

BRAND_RULES = {

    "SIEMENS": {
        "prefixes": ["6ES", "6AV", "3RT", "3RV", "3RW", "3VL"],
        "series": ["S7", "SIMATIC", "SIRIUS"]
    },

    "ALLEN BRADLEY": {
        "prefixes": ["1756", "1769", "1746", "1734"],
        "series": ["CONTROLLOGIX", "COMPACTLOGIX"]
    },

    "SCHNEIDER ELECTRIC": {
        "prefixes": ["LC1", "BMX", "TSX"],
        "series": ["TESYS", "MODICON"]
    },

    "OMRON": {
        "prefixes": ["E2E", "CP1", "CJ2"],
        "series": ["SYSMAC"]
    },

    "ABB": {
        "prefixes": ["ACS", "AF", "SACE"],
        "series": ["ACS DRIVES"]
    },

    "YASKAWA": {
        "prefixes": ["SGD", "SGM"],
        "series": ["SIGMA"]
    },

    "EATON": {
        "prefixes": ["DIL", "NZM"],
        "series": ["MOELLER"]
    },

    "PHOENIX CONTACT": {
        "prefixes": ["QUINT", "MINI"]
    },

    "WAGO": {
        "prefixes": ["750"]
    },

    "TURCK": {
        "prefixes": ["BI", "NI"]
    },

    "SICK": {
        "prefixes": ["IME", "WTB"]
    },

    "LEUZE": {
        "prefixes": ["PRK", "ODS"]
    },

    "PEPPERL+FUCHS": {
        "prefixes": ["NBB"]
    },

    "VEGA": {
        "prefixes": ["VEG"]
    },

    "ENDRESS+HAUSER": {
        "prefixes": ["PMC", "FMR"]
    },

    "PARKER": {
        "prefixes": ["PSD"]
    },

    "LENZE": {
        "prefixes": ["E82", "E94"]
    },

    "CONTROL TECHNIQUES": {
        "prefixes": ["UNI", "SP"]
    },

    "KOLLMORGEN": {
        "prefixes": ["AKM"]
    },

    "NIDEC": {
        "prefixes": ["M7"]
    }

}


CATEGORY_RULES = {

    "PLC": ["6ES", "1756", "1769", "BMX", "CJ2", "CP1"],

    "HMI": ["6AV", "NB", "MT"],

    "DRIVE": ["ACS", "E82", "E94", "UNI"],

    "CONTACTOR": ["3RT", "LC1", "AF", "DIL"],

    "SENSOR": ["E2E", "BI", "NBB", "IME", "PRK"],

    "POWER SUPPLY": ["QUINT", "MINI"],

    "IO MODULE": ["1734", "750"],

    "SAFETY": ["PNOZ"],

    "MOTOR": ["SGM", "AKM"]

}


# =========================
# BRAND DETECTION
# =========================

def detect_brand(part_number: str):

    if not part_number:
        return "Industrial"

    p = part_number.upper()

    for brand, data in BRAND_RULES.items():

        prefixes = data.get("prefixes", [])

        for prefix in prefixes:

            if p.startswith(prefix):

                return brand

    return "Industrial"


# =========================
# CATEGORY DETECTION
# =========================

def detect_category(part_number: str):

    if not part_number:
        return "Industrial Component"

    p = part_number.upper()

    for category, prefixes in CATEGORY_RULES.items():

        for prefix in prefixes:

            if p.startswith(prefix):

                return category

    return "Industrial Component"