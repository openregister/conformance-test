import csv
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

class TestEntryResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.csv'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/csv', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema):
        problems = entry_csv_schema.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Entry resource csv'

class TestEntryResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.tsv'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/tab-separated-values', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema):
        problems = entry_csv_schema.validate(csv.reader(response.text.split('\n'), delimiter='\t'))
        assert problems == [], \
            'There is a problem with Entry resource tsv'

class TestEntryResourceTtl(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.ttl'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/turtle', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_ttl_schema):
        namespace = 'https://openregister.github.io/specification/#'
        entry_ttl_schema.add_data(response.text)
        problems = entry_ttl_schema.validateDataMatchesFieldDataTypes(namespace)

        assert problems == [], \
            'There is a problem with Entry resource ttl'

