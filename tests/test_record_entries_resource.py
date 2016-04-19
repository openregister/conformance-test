import csv
import pytest
import requests
import re
import yaml

from urllib.parse import urljoin
from jsonschema import validate
from werkzeug.http import parse_options_header

class TestRecordEntriesResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s/entries.json' % item_json[register_name]))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, entries_schema):
        validate(response.json(), entries_schema)

class TestRecordEntriesResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s/entries.yaml' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/yaml', {'charset':'UTF-8'})

    def test_response_contents(self, response, entries_schema):
        validate(yaml.load(response.text), entries_schema)

class TestRecordEntriesResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s/entries.csv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/csv', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema):
        problems = entry_csv_schema.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Record Entries resource csv'

class TestRecordEntriesResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s/entries.tsv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/tab-separated-values', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema):
        problems = entry_csv_schema.validate(csv.reader(response.text.split('\n'), delimiter='\t'))
        assert problems == [], \
            'There is a problem with Record Entries resource tsv'