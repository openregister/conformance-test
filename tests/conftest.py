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
            **types.ENTRY_NUMBER,
            **types.ITEM_HASH,
            **types.ENTRY_TIMESTAMP,
            **types.ENTRY_KEY
        },
        'required': ['entry-number', 'item-hash', 'entry-timestamp', 'key'],
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
                **types.ENTRY_NUMBER,
                **types.ITEM_HASH,
                **types.ENTRY_TIMESTAMP,
                **types.ENTRY_KEY
            },
            'required': ['entry-number', 'item-hash', 'entry-timestamp', 'key'],
            'additionalProperties': False
        }
    }


@pytest.fixture(scope='session')
def record_entry_part_schema():
    return {
        'type': 'object',
        'properties': {
            **types.ENTRY_NUMBER,
            **types.ITEM_HASH,
            **types.ENTRY_TIMESTAMP,
        },
        'required': ['entry-number', 'item-hash', 'entry-timestamp'],
        'additionalProperties': False
    }


@pytest.fixture(scope='session')
def entry_csv_schema():
    validator = CSVValidator(('entry-number', 'entry-timestamp', 'item-hash', 'key'))
    validator.add_header_check()
    validator.add_value_check('entry-number', str, match_pattern('^\d+$'))
    validator.add_value_check('item-hash', str, match_pattern('^sha-256:[a-f\d]{64}$'))
    validator.add_value_check('entry-timestamp', str, match_pattern('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'))
    validator.add_value_check('key', str, match_pattern('.+'))
    return validator


@pytest.fixture(scope="session")
def entry_ttl_schema():
    validator = TtlValidator()
    validator.add_entry_regex('entry-number-field', '^\d+$')
    validator.add_entry_regex('entry-timestamp-field', '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
    validator.add_entry_regex('item-resource', '/item/sha-256:[a-f\d]{64}$')
    validator.add_entry_regex('key-field', '.+')
    return validator


@pytest.fixture(scope="session")
def record_ttl_schema():
    validator = TtlValidator()
    validator.add_entry_regex('entry-number-field', '^\d+$')
    validator.add_entry_regex('entry-timestamp-field', '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
    validator.add_entry_regex('item-resource', '/item/sha-256:[a-f\d]{64}$')
    return validator
