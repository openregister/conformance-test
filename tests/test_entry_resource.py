import pytest
import requests
import yaml

from jsonschema import validate
from urllib.parse import urljoin
from werkzeug.http import parse_options_header

class TestEntryResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, entry_schema):
        validate(response.json(), entry_schema)


class TestEntryResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.yaml'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/yaml', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_schema):
        validate(yaml.load(response.text), entry_schema)
