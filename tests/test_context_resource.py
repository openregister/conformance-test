import csv
import pytest
import requests
import warnings

from csvvalidator import CSVValidator
from urllib.parse import urljoin
from jsonschema import validate
from multihash import multihash


@pytest.mark.version(2)
class TestContextResourceJSON:
    def test_response_contents(self, context_schema, endpoint):
        response = requests.get(urljoin(endpoint, 'context'))
        parsed_response = response.json()
        validate(parsed_response, context_schema)

    def test_content_type(self, endpoint):
        response = requests.get(urljoin(endpoint, 'context'))
        assert response.headers['content-type'] == 'application/json'