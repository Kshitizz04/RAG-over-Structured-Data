# utils.py

def format_units(text: str) -> str:
    """
    Ensures all units in the response are consistent and readable.
    """
    return text.replace(" t ", " tonnes ").replace(" t/cm", " tonnes/cm")

def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Example: convert 1000 kg to tons
    """
    conversions = {
        ("kg", "tonnes"): lambda x: x / 1000,
        ("tonnes", "kg"): lambda x: x * 1000,
    }

    func = conversions.get((from_unit, to_unit))
    return func(value) if func else value
