def get_related_parts(part_number):

    prefix = part_number[:6]

    return {
        "type": "related",
        "prefix": prefix
    }


def get_replacement_parts(part_number):

    if "315" in part_number:

        return [
            "6ES7-315-2EH14-0AB0",
            "6ES7-315-6FF04-0AB0"
        ]

    return []


def get_accessories(part_number):

    if part_number.startswith("6ES7"):

        return [
            "6ES7-972-0BB12-0XA0",
            "6ES7-972-0BA52-0XA0"
        ]

    return []


def get_compatible_modules(part_number):

    if part_number.startswith("6ES7"):

        return [
            "SM321",
            "SM322",
            "SM331",
            "SM332"
        ]

    return []