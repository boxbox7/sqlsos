from .exceptions import TableFieldMultiPKException
from .exceptions import FieldTypeException
from .exceptions import FieldNotExistException
from .utils import get_class_fields


class Sql:
    """
    just support sqlite,
    because i only use it now...
    anyway maybe i will add others, haha...
    """
    pass


class BaseTableSQL(Sql):
    CREATE_SQL = 'CREATE TABLE {table_name} ({fields});'
    DROP_SQL = 'DROP TABLE {table_name};'
    INSERT_SQL = 'INSERT INTO {table_name} ({fields}) VALUES ({values});'
    INSERT_INTO_SQL = 'INSERT INTO {to_table_name} {to_fields} SELECT {from_fields} FROM {from_table_name}'
    SELECT_SQL = 'SELECT {fields} FROM {table_name}'


class SQLiteFieldType:
    INTEGER = 'INTEGER'
    REAL = 'REAL'
    NULL = 'NULL'
    TEXT = 'TEXT'
    BLOB = 'BLOB'
    NUMERIC = 'NUMERIC'


class Field:
    """
    table`s field instance
    ::
    >>> from sqlsos import Field
    >>> f = Field('first_name', Field.TYPE.TEXT)
    """
    TYPE = SQLiteFieldType

    def __init__(self,
                 name,
                 type,
                 /,
                 pk=False,
                 null=False,
                 auto_increment=False
                 ):
        self.name = name
        if type not in get_class_fields(SQLiteFieldType):
            raise FieldTypeException(f'{type} is not supported.')
        self.type = type
        self.pk = pk
        self.null = null
        self.auto_increment = auto_increment

    def _cov_null(self) -> str:
        if not self.null and not self.auto_increment:
            return 'NOT NULL'
        return ''

    def _cov_auto_increment(self) -> str:
        if self.auto_increment:
            return 'AUTOINCREMENT'
        return ''

    def _cov_pk(self):
        return "PRIMARY KEY" if self.auto_increment else ""

    def dump(self):
        fields = [self.name,
                  self.type,
                  self._cov_pk(),
                  self._cov_null(),
                  self._cov_auto_increment()]
        data = (d for d in fields if d)
        s = " ".join(data)
        return s


class FieldSet:
    """ todo:create a collection of field"""

    def __init__(self, *field):
        pass


class Table:
    def __init__(self, table_name, *fields):
        self.table_name = table_name
        if not self.is_pk_only_or_zero(fields):
            raise TableFieldMultiPKException()
        self.fields = tuple(fields)
        for field in self.fields:
            setattr(self, field.name, None)

    def __repr__(self):
        return f'<{self.table_name} {id(self)}>'

    def is_pk_only_or_zero(self, fields=None):
        if fields is None:
            fields = self.fields
        return len([field for field in fields if field.pk]) <= 1

    def create(self):
        if not self.is_pk_only_or_zero():
            raise TableFieldMultiPKException()
        fields_str = ', '.join(field.dump() for field in self.fields)
        return BaseTableSQL.CREATE_SQL.format(table_name=self.table_name,
                                              fields=fields_str)

    def drop(self):
        return BaseTableSQL.DROP_SQL.format(table_name=self.table_name)

    def insert(self, **kwargs):
        for field in kwargs.keys():
            if field not in dir(self):
                raise FieldNotExistException(f'{field} is not a valid field')
        fields = (k for k in kwargs.keys())
        values = (str(repr(v)) for v in kwargs.values())
        fields_str = ', '.join(fields)
        values_str = ', '.join(values)
        return BaseTableSQL.INSERT_SQL.format(table_name=self.table_name,
                                              fields=fields_str,
                                              values=values_str)

    def select(self, field):
        return Query(self, field)


class Query:
    # todo
    def __init__(self,
                 table=None,
                 fields=None):
        self.table = table
        self.fields = fields or []
        self._from = False
        self._where = False
