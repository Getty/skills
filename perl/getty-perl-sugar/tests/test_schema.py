"""Validate generated schemas against Draft 2020-12 using the real validator."""
from pathlib import Path
import json
import subprocess
import unittest
try:
    from jsonschema import Draft202012Validator, ValidationError
except ImportError:
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parents[1]

@unittest.skipIf(Draft202012Validator is None, 'jsonschema is not installed')
class GeneratedSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = subprocess.check_output(['perl', str(ROOT/'examples/reference/schema-demo.pl')], text=True)
        cls.schema = json.loads(raw)
        cls.validator = Draft202012Validator(cls.schema)

    def test_schema_validity(self):
        Draft202012Validator.check_schema(self.schema)

    def test_valid_input(self):
        self.validator.validate({'name':'Example','count':1,'mode':'fast','enabled':False})

    def test_nullable_enum_accepts_null(self):
        self.validator.validate({'name':'Example','count':1,'mode':None,'note':None})

    def test_null_is_not_omission(self):
        with self.assertRaises(ValidationError):
            self.validator.validate({'name':'Example','count':1})

    def test_invalid_cases(self):
        cases = [
            {'name':'x','count':0,'mode':'fast'},
            {'name':'x','count':1.5,'mode':'fast'},
            {'name':'','count':1,'mode':'fast'},
            {'name':'x'*61,'count':1,'mode':'fast'},
            {'name':'x','count':1,'mode':'unknown'},
            {'name':'x','count':1,'mode':'fast','extra':1},
            {'name':'x','count':1,'mode':'fast','enabled':0},
            {'name':'x','count':1,'mode':'fast','tags':['x']*6},
        ]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ValidationError):
                self.validator.validate(data)

if __name__ == '__main__':
    unittest.main()
