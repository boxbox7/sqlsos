from .models import Table, Field


def select(table, fields):
    field_set = [Field(field) for field in fields]
    return Table(table, *field_set).select(*fields)
