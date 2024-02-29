from .exceptions import TableOperationRepeatedException


class QueryWhereAbleMixin:
    def __init__(self, *args, **kwargs):
        self._where = False
        self._where_data = {}
        super().__init__(*args, **kwargs)

    def where(self, **kwargs):
        if not getattr(self, '_table'):
            raise AttributeError('miss _table attribute, `where` will be not valid')
        if self._where:
            raise TableOperationRepeatedException('where')
        self._table.check_input_fields(kwargs.keys())
        self._where_data.update(kwargs)
        self._where = True
        return self

    def _dump_where(self):
        if self._where and self._where_data:
            data = (f'{k} = {str(repr(v))}' for k, v in self._where_data.items())
            sql = ' WHERE ' + ' AND '.join(data)
            return sql
        else:
            return ''


class QueryOrderByAbleMixin:
    def __init__(self, *args, **kwargs):
        self._order_by = False
        self._order_by_data = {}
        super().__init__(*args, **kwargs)

    def order_by(self, **kwargs):
        if not getattr(self, '_table'):
            raise AttributeError('miss _table attribute, `order_by` will be not valid')
        if self._order_by:
            raise TableOperationRepeatedException('_order_by')
        self._table.check_input_fields(kwargs.keys())
        self._order_by_data.update(kwargs)
        self._order_by = True
        return self

    def _dump_order_by(self):
        if self._order_by and self._order_by_data:
            """todo"""


class QueryGroupByAbleMixin:
    def __init__(self, *args, **kwargs):
        self._group_by = False
        self._group_by_data = []
        super().__init__(*args, **kwargs)

    def group_by(self, *args):
        if not getattr(self, '_table'):
            raise AttributeError('miss _table attribute, `group_by` will be not valid')
        if self._group_by:
            raise TableOperationRepeatedException('group_by')
        self._table.check_input_fields(args)
        self._group_by_data.append(args)
        self._group_by = True
        return self
