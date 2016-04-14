import csv
import pytest
import requests
import re
import yaml

from csvvalidator import *
from jsonschema import validate
from urllib.parse import urljoin
from werkzeug.http import parse_options_header

class TestRecordResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.json' % item_json[register_name]))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, endpoint, entry_schema):
        record_json = response.json()

        entry_part = {
            'entry-number': record_json.pop('entry-number'),
            'item-hash': record_json.pop('item-hash'),
            'entry-timestamp': record_json.pop('entry-timestamp')
        }

        validate(entry_part, entry_schema)

        register_data = requests.get(urljoin(endpoint, '/register.json'))

        register_fields = register_data.json()['record']['entry']['fields']

        assert set(record_json.keys()).issubset(register_fields), \
            'Record contains unrecognized keys'

class TestRecordResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.yaml' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/yaml', {'charset':'UTF-8'})

    def test_response_contents(self, response, endpoint, entry_schema):
        record_yaml = yaml.load(response.text)

        entry_part = {
            'entry-number': record_yaml.pop('entry-number'),
            'item-hash': record_yaml.pop('item-hash'),
            'entry-timestamp': record_yaml.pop('entry-timestamp')
        }

        validate(entry_part, entry_schema)

        register_data = requests.get(urljoin(endpoint, '/register.json'))

        register_fields = register_data.json()['record']['entry']['fields']

        assert set(record_yaml.keys()).issubset(register_fields), \
            'Record contains unrecognized keys'

class TestRecordResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.csv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/csv', {'charset':'UTF-8'})

    def test_response_contents(self, response, endpoint, entry_schema):
        field_names = ['entry-number', 'item-hash', 'entry-timestamp']
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['record']['entry']['fields']
        field_names += register_fields

        validator = CSVValidator(field_names)
        validator.add_header_check()
        validator.add_value_check('entry-number', str, match_pattern('^\d+$'))
        validator.add_value_check('item-hash', str, match_pattern('^sha-256:[a-f\d]{64}$'))
        validator.add_value_check('entry-timestamp', str, match_pattern('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'))
        problems = validator.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Record resource csv'