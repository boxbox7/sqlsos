class FieldTypeException(Exception):
    """type of field is not support"""

class FieldNotExistException(Exception):
    pass


class TableFieldMultiPKException(Exception):
    """the exception about table have multiple primary key"""

