import pytest
import requests
import yaml

from jsonschema import validate
from urllib.parse import urljoin
from werkzeug.http import parse_options_header

# This schema should always represent the response json specified at <http://openregister.github.io/specification/#entry-resource>
ENTRY_SCHEMA = {
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

class TestEntryResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response):
        validate(response.json(), ENTRY_SCHEMA)


class TestEntryResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.yaml'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/yaml', {'charset':'UTF-8'})

    def test_response_contents(self, response):
        validate(yaml.load(response.text), ENTRY_SCHEMA)
