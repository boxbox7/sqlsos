class Sql:
    """
    just support sqlite,
    because i only use it now...
    anyway maybe i will add others, haha...
    """
    pass


class BaseTableSQL(Sql):
    """
    base table-sql have no `where` `order by` balabala..
    """
    CREATE_SQL = 'CREATE TABLE {table_name} ({fields});'
    DROP_SQL = 'DROP TABLE {table_name};'
    INSERT_SQL = 'INSERT INTO {table_name} (ID, {fields}) VALUES (NULL, {values});'
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

    def __str__(self):
        return self.dump()


class FieldSet:
    """ todo:create a collection of field"""

    def __init__(self, *field):
        pass


class Table:
    def __init__(self, name, *fields):
        self.name = name
        if not self.is_pk_only_or_zero(fields):
            raise TableFieldMultiPKException()
        self.fields = tuple(fields)

    def __str__(self):
        return f'<{self.name}>'

    def is_pk_only_or_zero(self, fields=None):
        if fields is None:
            fields = self.fields
        return len([field for field in fields if field.pk]) <= 1

    def create(self):
        if not self.is_pk_only_or_zero():
            raise TableFieldMultiPKException()
        return BaseTableSQL.CREATE_SQL.format(table_name=self.name,
                                              fields=self.fields)


class FieldTypeException(Exception):
    """type of field is not support"""


class TableFieldMultiPKException(Exception):
    """the exception about table have multiple primary key"""


def get_class_fields(cls):
    for t in dir(cls):
        if not t.startswith('__'):
            yield t


def make_default_id_fields() -> Field:
    """
    make a `id` field
    :return:
    """
    f = Field('id', Field.TYPE.INTEGER, pk=True, auto_increment=True)
    return f
