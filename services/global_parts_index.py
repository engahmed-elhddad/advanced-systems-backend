import random


# =========================================================
# GLOBAL INDUSTRIAL BRANDS DATABASE
# =========================================================

INDUSTRIAL_BRANDS = {

    "SIEMENS": {
        "PLC": ["6ES7"],
        "HMI": ["6AV"],
        "CONTACTOR": ["3RT"],
        "OVERLOAD": ["3RU"],
        "DRIVE": ["6SL"],
        "POWER": ["6EP"]
    },

    "SCHNEIDER": {
        "PLC": ["BMX", "BME"],
        "CONTACTOR": ["LC1"],
        "DRIVE": ["ATV"],
        "RELAY": ["RXM"]
    },

    "ALLEN_BRADLEY": {
        "PLC": ["1756", "1769"],
        "IO": ["1734"],
        "DRIVE": ["22B"],
        "SAFETY": ["440"]
    },

    "OMRON": {
        "PLC": ["CP1", "CJ2"],
        "SENSOR": ["E2E", "E3Z"],
        "SAFETY": ["G9"]
    },

    "ABB": {
        "DRIVE": ["ACS"],
        "CONTACTOR": ["AF"],
        "BREAKER": ["SACE"]
    },

    "PILZ": {
        "SAFETY": ["PNOZ"]
    },

    "ENDRESS_HAUSER": {
        "FLOW": ["FMP", "FMR"],
        "PRESSURE": ["PMC"]
    },

    "PEPPERL_FUCHS": {
        "SENSOR": ["NBB", "NBN"]
    },

    "TURCK": {
        "SENSOR": ["BI", "NI"]
    },

    "SICK": {
        "SENSOR": ["WT", "VL"]
    },

    "IFM": {
        "SENSOR": ["IF", "SI"]
    },

    "FESTO": {
        "PNEUMATIC": ["DSNU", "ADN"]
    },

    "SMC": {
        "PNEUMATIC": ["CDQ", "SY"]
    },

    "KEYENCE": {
        "SENSOR": ["FS", "IV"]
    },

    "MITSUBISHI": {
        "PLC": ["FX", "Q"]
    },

    "VEGA": {
        "LEVEL": ["VEGAPULS", "VEGABAR"]
    },

    "BECKHOFF": {
        "IO": ["EL", "EK"]
    },

    "BOSCH_REXROTH": {
        "DRIVE": ["R911"]
    },

    "WAGO": {
        "IO": ["750"]
    },

    "PHOENIX_CONTACT": {
        "POWER": ["QUINT", "MINI"]
    },

    "LENZE": {
        "DRIVE": ["E84"]
    },

    "YOKOGAWA": {
        "TRANSMITTER": ["EJA"]
    },

    "BR_AUTOMATION": {
        "PLC": ["X20"]
    }

}


# =========================================================
# PART GENERATOR
# =========================================================

def generate_part(prefix):

    number = random.randint(10, 9999)

    return f"{prefix}{number}"


# =========================================================
# BRAND PART GENERATOR
# =========================================================

def generate_brand_parts(prefixes):

    parts = []

    for prefix in prefixes:

        for i in range(30):

            parts.append(generate_part(prefix))

    return parts


# =========================================================
# GLOBAL PART GENERATOR
# =========================================================

def generate_global_parts():

    parts = []

    for brand in INDUSTRIAL_BRANDS:

        categories = INDUSTRIAL_BRANDS[brand]

        for category in categories:

            prefixes = categories[category]

            parts += generate_brand_parts(prefixes)

    return list(set(parts))