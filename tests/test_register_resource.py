import pytest
import requests

import tests.data_types as types
from jsonschema import validate
from urllib.parse import urljoin

REGISTER_RESOURCE_SCHEMA = {
    'type': 'object',
    'required': ['domain', 'last-updated', 'total-records', 'total-entries', 'total-items', 'register-record'],
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


@pytest.mark.version(1)
class TestRegisterResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'register.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    @pytest.mark.xfail(reason='Missing total-items')
    def test_response_contents(self, response):
        validate(response.json(), REGISTER_RESOURCE_SCHEMA)