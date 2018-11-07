import pytest

import tests.data_types as types
from csvvalidator import *
from .ttlvalidator import TtlValidator


def pytest_addoption(parser):
    parser.addoption('--endpoint', action='append', help='register endpoints to test')
    parser.addoption('--register', action='append', help='Name of register')
    parser.addoption('--register-domain', action='append', help='Register domain')
    parser.addoption('--api-version', action='store', help='Register API version', type=int)


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers",
        "version(name): mark test to apply to a specific API version")

def pytest_runtest_setup(item):
    api_versions = [mark.args[0] for mark in item.iter_markers(name='version')]
    checked_version = item.config.getoption('--api-version')
    if checked_version not in api_versions:
        pytest.skip("test requires --api-version in %r" % api_versions)

def pytest_generate_tests(metafunc):
    if 'endpoint' in metafunc.fixturenames:
        endpoints = metafunc.config.option.endpoint
        metafunc.parametrize('endpoint', endpoints)

    if 'register' in metafunc.fixturenames:
        metafunc.parametrize('register', metafunc.config.option.register)

    if 'register_domain' in metafunc.fixturenames:
        metafunc.parametrize('register_domain', metafunc.config.option.register_domain)


@pytest.fixture(scope='session')
def entry_schema_v1():
    return {
            'type': 'array',
            'minItems': 1,
            'maxItems': 1,
            'items': {
                'type': 'object',
                'properties': {
                    **types.INDEX_ENTRY_NUMBER,
                    **types.ENTRY_NUMBER,
                    **types.ITEM_HASH_ARRAY,
                    **types.ENTRY_TIMESTAMP,
                    **types.ENTRY_KEY
                },
                'required': ['index-entry-number','entry-number', 'item-hash', 'entry-timestamp', 'key'],
                'additionalProperties': False
            }
        }

@pytest.fixture(scope='session')
def entry_schema_v2():
    return {
            'type': 'array',
            'minItems': 1,
            'maxItems': 1,
            'items': {
                'type': 'object',
                'properties': {
                    **types.INDEX_ENTRY_NUMBER,
                    **types.ENTRY_NUMBER,
                    **types.BLOB_HASH_ARRAY,
                    **types.ENTRY_TIMESTAMP,
                    **types.ENTRY_KEY
                },
                'required': ['index-entry-number','entry-number', 'blob-hash', 'entry-timestamp', 'key'],
                'additionalProperties': False
            }
        }


@pytest.fixture(scope='session')
def entries_schema_v1():
    return {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                **types.INDEX_ENTRY_NUMBER,
                **types.ENTRY_NUMBER,
                **types.ITEM_HASH_ARRAY,
                **types.ENTRY_TIMESTAMP,
                **types.ENTRY_KEY
            },
            'required': ['index-entry-number','entry-number', 'item-hash', 'entry-timestamp', 'key'],
            'additionalProperties': False
        }
    }


@pytest.fixture(scope='session')
def entries_schema_v2():
    return {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                **types.INDEX_ENTRY_NUMBER,
                **types.ENTRY_NUMBER,
                **types.BLOB_HASH_ARRAY,
                **types.ENTRY_TIMESTAMP,
                **types.ENTRY_KEY
            },
            'required': ['index-entry-number','entry-number', 'blob-hash', 'entry-timestamp', 'key'],
            'additionalProperties': False
        }
    }


@pytest.fixture(scope='session')
def record_schema():
    return {
        'type': 'object',
        'patternProperties': {
            ".*": {
                'properties': {
                    **types.INDEX_ENTRY_NUMBER,
                    **types.ENTRY_NUMBER,
                    **types.ENTRY_KEY,
                    **types.ENTRY_TIMESTAMP,
                    **types.ITEM
                },
                'required': ['index-entry-number', 'entry-number', 'key', 'entry-timestamp'],
                'additionalProperties': False
            }
        },
        'additionalProperties': False
    }


@pytest.fixture(scope='session')
def entry_csv_schema_v1():
    validator = CSVValidator(('index-entry-number', 'entry-number', 'entry-timestamp', 'key', 'item-hash'))
    validator.add_header_check()
    validator.add_value_check('index-entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('item-hash', str, match_pattern(types.HASH_PATTERN))
    validator.add_value_check('entry-timestamp', str, match_pattern(types.TIMESTAMP_PATTERN))
    validator.add_value_check('key', str, match_pattern(types.KEY_PATTERN))
    return validator


@pytest.fixture(scope='session')
def entry_csv_schema_v2():
    validator = CSVValidator(('index-entry-number', 'entry-number', 'entry-timestamp', 'key', 'blob-hash'))
    validator.add_header_check()
    validator.add_value_check('index-entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('blob-hash', str, match_pattern(types.HASH_PATTERN))
    validator.add_value_check('entry-timestamp', str, match_pattern(types.TIMESTAMP_PATTERN))
    validator.add_value_check('key', str, match_pattern(types.KEY_PATTERN))
    return validator


@pytest.fixture(scope='session')
def entry_ttl_schema():
    validator = TtlValidator()
    validator.add_entry_regex('entry-number-field', types.ENTRY_NUMBER_PATTERN)
    validator.add_entry_regex('entry-timestamp-field', types.TIMESTAMP_PATTERN)
    validator.add_entry_regex('item-resource', types.ITEM_RESOURCE_PATTERN)
    validator.add_entry_regex('key-field', types.KEY_PATTERN)
    return validator


@pytest.fixture(scope='session')
def record_ttl_schema():
    validator = TtlValidator()
    validator.add_entry_regex('entry-number-field', types.ENTRY_NUMBER_PATTERN)
    validator.add_entry_regex('entry-timestamp-field', types.TIMESTAMP_PATTERN)
    validator.add_entry_regex('item-resource', types.ITEM_RESOURCE_PATTERN)
    return validator
