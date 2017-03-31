import pytest

import tests.data_types as types
from csvvalidator import *
from .ttlvalidator import TtlValidator


def pytest_addoption(parser):
    parser.addoption('--endpoint', action='append', help='register endpoints to test')
    parser.addoption('--register', action='append', help='Name of register')
    parser.addoption('--register-domain', action='append', help='Register domain')


def pytest_generate_tests(metafunc):
    if 'endpoint' in metafunc.fixturenames:
        metafunc.parametrize('endpoint', metafunc.config.option.endpoint)

    if 'register' in metafunc.fixturenames:
        metafunc.parametrize('register', metafunc.config.option.register)

    if 'register_domain' in metafunc.fixturenames:
        metafunc.parametrize('register_domain', metafunc.config.option.register_domain)


@pytest.fixture(scope='session')
def entry_schema():
    # This schema should always represent the response json specified at
    # <http://openregister.github.io/specification/#entry-resource>
    return {
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


@pytest.fixture(scope='session')
def entries_schema():
    # This schema should always represent the response json specified at
    # <http://openregister.github.io/specification/#entries-resource>
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
def record_schema():
    return {
        'type': 'object',
        'properties': {
            **types.INDEX_ENTRY_NUMBER,
            **types.ENTRY_NUMBER,
            **types.ENTRY_KEY,
            **types.ENTRY_TIMESTAMP,
        },
        'required': ['index-entry-number', 'entry-number', 'key', 'entry-timestamp'],
        'additionalProperties': False
    }


@pytest.fixture(scope='session')
def entry_csv_schema():
    validator = CSVValidator(('index-entry-number', 'entry-number', 'entry-timestamp', 'key', 'item-hash'))
    validator.add_header_check()
    validator.add_value_check('index-entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('item-hash', str, match_pattern(types.HASH_PATTERN))
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
