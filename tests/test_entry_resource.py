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
        return requests.get(urljoin(endpoint, 'entries/1.json'))

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    @pytest.mark.version(1)
    def test_response_contents(self, response, entry_schema_v1):
        validate(response.json(), entry_schema_v1)

    @pytest.mark.version(2)
    def test_response_contents(self, response, entry_schema_v2):
        validate(response.json(), entry_schema_v2)


@pytest.mark.version(1)
class TestEntryResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries/1.yaml'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/yaml', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_schema_v1):
        validate(yaml.load(response.text), entry_schema_v1)


class TestEntryResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries/1.csv'))

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    @pytest.mark.version(1)
    def test_response_contents(self, response, entry_csv_schema_v1):
        problems = entry_csv_schema_v1.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Entry resource csv'

    @pytest.mark.version(2)
    def test_response_contents(self, response, entry_csv_schema_v2):
        problems = entry_csv_schema_v2.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Entry resource csv'


@pytest.mark.version(1)
class TestEntryResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries/1.tsv'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/tab-separated-values', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema_v1):
        problems = entry_csv_schema_v1.validate(csv.reader(response.text.split('\n'), delimiter='\t'))
        assert problems == [], \
            'There is a problem with Entry resource tsv'


@pytest.mark.version(1)
class TestEntryResourceTtl(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries/1.ttl'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/turtle', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_ttl_schema):
        entry_ttl_schema.add_data(response.text)
        problems = entry_ttl_schema.validate_data_matches_field_data_types()

        assert problems == [], \
            'There is a problem with Entry resource ttl'
