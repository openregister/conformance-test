import pytest
import requests
import yaml

import tests.data_types as types
from jsonschema import validate
from urllib.parse import urljoin

REGISTER_RESOURCE_SCHEMA = {
    'type': 'object',
    'properties': {
        'domain': {
            'type': 'string'
        },
        'last-updated': {
            'type': 'string',
            'pattern': types.TIMESTAMP_PATTERN
        },
        'custodian': {
            'type': 'string',
            'required': false
        },
        'total-records': {'type': 'integer'},
        'total-entries': {'type': 'integer'},
        'total-items': {'type': 'integer'},
        'register-record': {
            'type': 'object',
            'properties': {
                **types.INDEX_ENTRY_NUMBER,
                **types.ENTRY_NUMBER,
                **types.ENTRY_KEY,
                **types.ENTRY_TIMESTAMP,
                'register': {'type': 'string'},
                'registry': {'type': 'string'},
                'phase': {'type': 'string'},
                'text': {'type': 'string'},
                'copyright': {'type': 'string'},
                'fields': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    }
                }
            },
            'additionalProperties': False
        }
    },
    'additionalProperties': False
}


class TestRegisterResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'register.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response):
        validate(response.json(), REGISTER_RESOURCE_SCHEMA)


class TestRegisterResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'register.yaml'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'text/yaml;charset=UTF-8'

    def test_response_contents(self, response):
        validate(yaml.load(response.text), REGISTER_RESOURCE_SCHEMA)
