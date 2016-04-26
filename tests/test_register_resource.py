import pytest
import requests
import yaml

from jsonschema import validate
from urllib.parse import urljoin

REGISTER_RESOURCE_SCHEMA = {
    "type": "object",
    "properties": {
        "domain": {
            "type": "string"
        },
        "last-updated": {
            "type": "string",
            "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
        },
        "total-records": {"type": "integer"},
        "total-entries": {"type": "integer"},
        "total-items": {"type": "integer"},
        "register-record": {
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
                },
                "register": {"type": "string"},
                "registry": {"type": "string"},
                "phase": {"type": "string"},
                "text": {"type": "string"},
                "copyright": {"type": "string"},
                "fields": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "additionalProperties": False
        }
    },
    "additionalProperties": False
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
