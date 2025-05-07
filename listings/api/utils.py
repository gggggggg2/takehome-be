def convert_to_int(string_value):
    try:
        val = int(string_value)
        return val
    except (ValueError, TypeError):
        return 0
