def str_to_bool(variable: str) -> bool:
    """Convert string variable to boolean.

    First check if variable contains "true" or "false" (converted to lower case) and return a value
    based on that.

    Otherwise attempt to convert variable to integer and then to boolean from that.

    Example:
    "True" -> True
    "true" -> True
    "False" -> False
    "false" -> False
    "1" -> True
    "0" -> False

    Args:
        variable: String variable to convert to boolean.
    Returns:
        Converted value.
    """
    if not isinstance(variable, str):
        raise TypeError("Variable must be a string.")

    lower_case = variable.lower()
    if lower_case == "true":
        return True
    elif lower_case == "false":
        return False
    return bool(int(variable))
