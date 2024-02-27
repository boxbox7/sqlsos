def get_class_fields(cls):
    for t in dir(cls):
        if not t.startswith('__'):
            yield t


def is_safe_field_type(_type):
    """
    >>> is_safe_field_type('CHAR(20)')
    True
    >>> is_safe_field_type('VARCHAR(29)')
    True
    >>> is_safe_field_type('CHA')
    False
    """
    t = tuple(_type)
    match t:
        case 'C', 'H', 'A', 'R', '(', *max_length, ')' if ''.join(max_length).isdigit():
            return True
        case 'V', 'A', 'R', 'C', 'H', 'A', 'R', '(', *max_length, ')' if ''.join(max_length).isdigit():
            return True
        case _:
            return False
