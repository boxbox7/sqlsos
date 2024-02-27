class FieldTypeException(Exception):
    """type of field is not support"""


class FieldNotExistException(Exception):
    pass


class TableFieldMultiPKException(Exception):
    """the exception about table have multiple primary key"""


class TableFieldParseException(Exception):
    """table accept obj is not Field instance"""


class TableOperationRepeatedException(Exception):
    pass