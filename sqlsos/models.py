from .exceptions import TableFieldMultiPKException
from .exceptions import FieldTypeException
from .exceptions import FieldNotExistException
from .exceptions import TableOperationRepeatedException
from .utils import get_class_fields
from .utils import is_safe_field_type


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
    CHAR = 'CHAR'
    VARCHAR = 'VARCHAR'


class Field:
    def __init__(self,
                 name,
                 /,
                 pk=False,
                 null=False,
                 auto_increment=False):
        self.name = name
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
        raise NotImplementedError


class TypedField(Field):
    """
    table`s field instance
    ::
    >>> from sqlsos import TypedField
    >>> f = TypedField('first_name', TypedField.TYPE.TEXT)
    """
    TYPE = SQLiteFieldType

    def __init__(self,
                 name,
                 field_type,
                 /,
                 pk=False,
                 null=False,
                 auto_increment=False
                 ):
        if field_type not in get_class_fields(SQLiteFieldType) \
                and not is_safe_field_type(field_type):
            raise FieldTypeException(f'{field_type} is not supported.')
        self.type = field_type
        super().__init__(name, pk=pk, null=null, auto_increment=auto_increment)

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
            if isinstance(field, Field):
                setattr(self, field.name, None)
            else:
                raise FieldNotExistException()

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
        self.check_input_fields(kwargs.keys())
        fields = (k for k in kwargs.keys())
        values = (str(repr(v)) for v in kwargs.values())
        fields_str = ', '.join(fields)
        values_str = ', '.join(values)
        return BaseTableSQL.INSERT_SQL.format(table_name=self.table_name,
                                              fields=fields_str,
                                              values=values_str)

    def check_input_fields(self, fields):
        for field in fields:
            if field not in dir(self):
                raise FieldNotExistException(f'{field} is not a valid field')

    def select(self, *field):
        return Query(self, field)


class Query:
    # todo
    def __init__(self,
                 table=None,
                 fields=None):
        self.table = table
        self.fields = fields or []
        self._where = False
        self._where_data = {}
        self._order_by = False
        self._order_by_data = {}
        self._group_by = False

    def where(self, **kwargs):
        if self._where:
            raise TableOperationRepeatedException()
        self.table.check_input_fields(kwargs)
        self._where_data.update(kwargs)
        self._mute(self.where)
        return self

    def order_by(self, **kwargs):
        if self._order_by:
            raise TableOperationRepeatedException()
        self.table.check_input_fields(kwargs.keys())
        self._order_by_data.update(kwargs)
        self._mute(self.order_by)
        return self

    def to_sql(self):
        """ todo """

    def _mute(self, func):
        setattr(self, f'_{func.__name__}', True)
