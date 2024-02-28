import unittest
import sqlsos as ss
from sqlsos.exceptions import FieldTypeException


class TestField(unittest.TestCase):
    def test_field_init(self):
        f = ss.Field('name', ss.Field.TYPE.VARCHAR, pk=True, null=True, auto_increment=True)
        self.assertEqual(f._name, 'name')  # add assertion here
        self.assertEqual(f._type, ss.Field.TYPE.VARCHAR)
        self.assertEqual(f._pk, True)
        self.assertEqual(f._null, True)
        self.assertEqual(f._auto_increment, True)

    def test_field_input_error_type(self):
        with self.assertRaises(FieldTypeException):
            f = ss.Field('name', 'a error type')

    def test_cov_null(self):
        # test not null
        f = ss.Field('name', ss.Field.TYPE.VARCHAR)
        result = f._cov_null()
        self.assertEqual(result, 'NOT NULL')
        # test null
        f2 = ss.Field('name', ss.Field.TYPE.VARCHAR, null=True)
        result2 = f2._cov_null()
        self.assertEqual(result2, '')

    def test_cov_auto_increment(self):
        f = ss.Field('name', ss.Field.TYPE.VARCHAR, auto_increment=True)
        result = f._cov_auto_increment()
        self.assertEqual(result, 'AUTOINCREMENT')
        f2 = ss.Field('name', ss.Field.TYPE.VARCHAR)
        result2 = f2._cov_auto_increment()
        self.assertEqual(result2, '')

    def test_cov_pk(self):
        f = ss.Field('name', ss.Field.TYPE.VARCHAR, pk=True)
        result = f._cov_pk()
        self.assertEqual(result, 'PRIMARY KEY')
        f2 = ss.Field('name', ss.Field.TYPE.VARCHAR)
        result2 = f2._cov_pk()
        self.assertEqual(result2, '')

    def test_dump(self):
        f = ss.Field('name', ss.Field.TYPE.VARCHAR)
        self.assertEqual(f.dump(),
                         "name VARCHAR NOT NULL")
        f2 = ss.Field('name', ss.Field.TYPE.TEXT, pk=True)
        self.assertEqual(f2.dump(),
                         "name TEXT PRIMARY KEY NOT NULL")
        f3 = ss.Field('name', ss.Field.TYPE.TEXT, auto_increment=True)
        self.assertEqual(f3.dump(),
                         "name TEXT PRIMARY KEY AUTOINCREMENT")


if __name__ == '__main__':
    unittest.main()
