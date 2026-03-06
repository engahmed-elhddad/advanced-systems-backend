def get_datasheet(part: str):

    part = part.upper()

    # Siemens PLC
    if part.startswith("6ES7"):
        return f"https://support.industry.siemens.com/cs/attachments/{part}/{part}.pdf"

    # Siemens Contactors
    if part.startswith("3RT"):
        return "https://cache.industry.siemens.com/dl/files/686/109476686/att_109476686/v1/3rt_contactors.pdf"

    # Schneider
    if part.startswith("LC1D"):
        return f"https://download.schneider-electric.com/files?p_Doc_Ref={part}"

    # Pepperl Fuchs
    if part.startswith("NBB"):
        return f"https://files.pepperl-fuchs.com/webcat/navi/productInfo/doct/{part}.pdf"

    # Mitsubishi
    if part.startswith("FX"):
        return "https://dl.mitsubishielectric.com/fa/document/manual/plc_fx_series.pdf"

    # Generic fallback
    return None