import csv
import pytest
import requests
import yaml

from urllib.parse import urljoin
from jsonschema import validate
from werkzeug.http import parse_options_header


class TestEntriesResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries.json'))

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    @pytest.mark.version(1)
    def test_response_contents(self, response, entries_schema_v1):
        validate(response.json(), entries_schema_v1)

    @pytest.mark.version(2)
    def test_response_contents(self, response, entries_schema_v2):
        validate(response.json(), entries_schema_v2)


@pytest.mark.version(1)
class TestEntriesResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries.yaml'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/yaml', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entries_schema_v1):
        validate(yaml.load(response.text), entries_schema_v1)


class TestEntriesResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries.csv'))

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    @pytest.mark.version(1)
    def test_response_contents(self, response, entry_csv_schema_v1):
        problems = entry_csv_schema_v1.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Entries resource csv'

    @pytest.mark.version(2)
    def test_response_contents(self, response, entry_csv_schema_v2):
        problems = entry_csv_schema_v2.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Entries resource csv'


@pytest.mark.version(1)
class TestEntriesResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries.tsv'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/tab-separated-values', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema_v1):
        problems = entry_csv_schema_v1.validate(csv.reader(response.text.split('\n'), delimiter='\t'))
        assert problems == [], \
            'There is a problem with Entries resource tsv'


@pytest.mark.version(1)
class TestEntriesResourceTtl(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries.ttl'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/turtle', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_ttl_schema):
        entry_ttl_schema.add_data(response.text)
        problems = entry_ttl_schema.validate_data_matches_field_data_types()

        assert problems == [], \
            'There is a problem with Entries resource ttl'
