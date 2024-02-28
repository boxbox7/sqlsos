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


if __name__ == '__main__':
    unittest.main()
