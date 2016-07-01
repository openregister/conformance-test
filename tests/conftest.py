import pytest

from csvvalidator import *


def pytest_addoption(parser):
    parser.addoption("--endpoint", action="append",
                     help="register endpoints to test")


def pytest_generate_tests(metafunc):
    if 'endpoint' in metafunc.fixturenames:
        metafunc.parametrize("endpoint",
                             metafunc.config.option.endpoint)


@pytest.fixture(scope="session")
def entry_schema():
    # This schema should always represent the response json specified at <http://openregister.github.io/specification/#entry-resource>
    return {
        "type": "object",
        "properties": {
            "entry-number": {
                "type": "string",
                "pattern": "^\d+$"
            },
            "item-hash": {
                "type": "string",
                "pattern": "^sha-256:[a-f\d]{64}$"
            },
            "entry-timestamp": {
                "type": "string",
                "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
            }
        },
        "required": ["entry-number", "item-hash", "entry-timestamp"],
        "additionalProperties": False
    }

@pytest.fixture(scope="session")
def entries_schema():
    # This schema should always represent the response json specified at <http://openregister.github.io/specification/#entries-resource>
    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "entry-number": {
                    "type": "string",
                    "pattern": "^\d+$"
                },
                "item-hash": {
                    "type": "string",
                    "pattern": "^sha-256:[a-f\d]{64}$"
                },
                "entry-timestamp": {
                    "type": "string",
                    "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
                }
            },
            "required": ["entry-number", "item-hash", "entry-timestamp"],
            "additionalProperties": False
        }
    }
    
@pytest.fixture(scope="session")
def entry_csv_schema():
    validator = CSVValidator(('entry-number', 'entry-timestamp', 'item-hash'))
    validator.add_header_check()
    validator.add_value_check('entry-number', str, match_pattern('^\d+$'))
    validator.add_value_check('item-hash', str, match_pattern('^sha-256:[a-f\d]{64}$'))
    validator.add_value_check('entry-timestamp', str, match_pattern('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'))
    return validator