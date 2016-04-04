import pytest
import requests

from urllib.parse import urljoin
from jsonschema import validate


class TestEntryResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    @pytest.mark.xfail
    def test_response_contents(self, response):
        #This schema should always represent the response json specified at <http://openregister.github.io/specification/#entry-resource>
        entry_schema = {
            "type": "object",
            "properties": {
                "entry-number": {
                    "type": "string",
                    "pattern": "^\d+$"
                },
                "item-hash": {
                    "type": "string",
                    "pattern": "^sha-256:[a-z\d]+$"
                },
                "entry-timestamp": {
                    "type": "string",
                    "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
                }
            },
            "required": ["entry-number", "item-hash", "entry-timestamp"],
            "additionalProperties": False
        }

        validate(response.json(), entry_schema)
