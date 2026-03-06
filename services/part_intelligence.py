def detect_part_info(part):

    part = part.upper()

    rules = [

        {
            "prefix": "6ES7",
            "manufacturer": "Siemens",
            "category": "PLC Module",
            "description": "Siemens SIMATIC S7 PLC automation module"
        },

        {
            "prefix": "3RT",
            "manufacturer": "Siemens",
            "category": "Contactor",
            "description": "Siemens industrial power contactor"
        },

        {
            "prefix": "NBB",
            "manufacturer": "Pepperl+Fuchs",
            "category": "Inductive Sensor",
            "description": "Pepperl+Fuchs inductive proximity sensor"
        },

        {
            "prefix": "FX",
            "manufacturer": "Mitsubishi",
            "category": "PLC Controller",
            "description": "Mitsubishi industrial PLC controller"
        },

        {
            "prefix": "LC1D",
            "manufacturer": "Schneider Electric",
            "category": "Contactor",
            "description": "Schneider TeSys industrial contactor"
        }

    ]

    for rule in rules:

        if part.startswith(rule["prefix"]):

            return {
                "manufacturer": rule["manufacturer"],
                "category": rule["category"],
                "description": rule["description"]
            }

    return {
        "manufacturer": None,
        "category": "Industrial Automation Component",
        "description": "Industrial automation spare part"
    }