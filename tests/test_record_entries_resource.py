import csv
import pytest
import requests
import yaml

from urllib.parse import urljoin
from jsonschema import validate
from werkzeug.http import parse_options_header


@pytest.mark.version(1)
class TestRecordEntriesResourceJsonV1(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'items/%s.json' % entry_json['item-hash'][0])).json()

        return requests.get(urljoin(endpoint, 'records/%s/entries.json' % item_json[register_name]))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, entries_schema_v1):
        validate(response.json(), entries_schema_v1)


@pytest.mark.version(2)
class TestRecordEntriesResourceJsonV2(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()
        blob_json = requests.get(urljoin(endpoint, 'blobs/%s.json' % entry_json['blob-hash'])).json()

        return requests.get(urljoin(endpoint, 'records/%s/entries.json' % blob_json[register_name]))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, entries_schema_v2):
        validate(response.json(), entries_schema_v2)


@pytest.mark.version(1)
class TestRecordEntriesResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'][0])).json()

        return requests.get(urljoin(endpoint, 'records/%s/entries.yaml' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/yaml', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entries_schema_v1):
        validate(yaml.load(response.text), entries_schema_v1)


@pytest.mark.version(1)
class TestRecordEntriesResourceCsvV1(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'][0])).json()

        return requests.get(urljoin(endpoint, 'records/%s/entries.csv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema_v1):
        problems = entry_csv_schema_v1.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Record Entries resource csv'


@pytest.mark.version(2)
class TestRecordEntriesResourceCsvV2(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()
        blob_json = requests.get(urljoin(endpoint, 'blobs/%s.json' % entry_json['blob-hash'])).json()

        return requests.get(urljoin(endpoint, 'records/%s/entries.csv' % blob_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema_v2):
        problems = entry_csv_schema_v2.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Record Entries resource csv'


@pytest.mark.version(1)
class TestRecordEntriesResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'][0])).json()

        return requests.get(urljoin(endpoint, 'records/%s/entries.tsv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/tab-separated-values', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema_v1):
        problems = entry_csv_schema_v1.validate(csv.reader(response.text.split('\n'), delimiter='\t'))
        assert problems == [], \
            'There is a problem with Record Entries resource tsv'


@pytest.mark.version(1)
class TestRecordEntriesResourceTtl(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'][0])).json()

        return requests.get(urljoin(endpoint, 'records/%s/entries.ttl' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/turtle', {'charset': 'UTF-8'})

    def test_response_contents(self, response, entry_ttl_schema):
        entry_ttl_schema.add_data(response.text)
        problems = entry_ttl_schema.validate_data_matches_field_data_types()

        assert problems == [], \
            'There is a problem with Record Entries resource ttl'
