import csv
import pytest
import requests
import yaml

from csvvalidator import *
from jsonschema import validate
from urllib.parse import urljoin
from werkzeug.http import parse_options_header

class TestRecordResourceJson(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.json' % item_json[register_name]))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, endpoint, record_entry_part_schema):
        record_json = response.json()

        entry_part = {
            'entry-number': record_json.pop('entry-number'),
            'item-hash': record_json.pop('item-hash'),
            'entry-timestamp': record_json.pop('entry-timestamp')
        }

        validate(entry_part, record_entry_part_schema)

        register_data = requests.get(urljoin(endpoint, '/register.json'))

        register_fields = register_data.json()['register-record']['fields']

        assert set(record_json.keys()).issubset(register_fields), \
            'Record contains unrecognized keys'

class TestRecordResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.yaml' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/yaml', {'charset':'UTF-8'})

    def test_response_contents(self, response, endpoint, record_entry_part_schema):
        record_yaml = yaml.load(response.text)

        entry_part = {
            'entry-number': record_yaml.pop('entry-number'),
            'item-hash': record_yaml.pop('item-hash'),
            'entry-timestamp': record_yaml.pop('entry-timestamp')
        }

        validate(entry_part, record_entry_part_schema)

        register_data = requests.get(urljoin(endpoint, '/register.json'))

        register_fields = register_data.json()['register-record']['fields']

        assert set(record_yaml.keys()).issubset(register_fields), \
            'Record contains unrecognized keys'

class TestRecordResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.csv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/csv', {'charset':'UTF-8'})

    def test_response_contents(self, response, endpoint):
        csvSchema = RecordCsvSchema.get_schema(self,endpoint)
        problems = csvSchema.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Record resource csv'

class TestRecordResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.tsv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/tab-separated-values', {'charset':'UTF-8'})

    def test_response_contents(self, response, endpoint):
        tsvSchema = RecordCsvSchema.get_schema(self, endpoint)
        problems = tsvSchema.validate(csv.reader(response.text.split('\n'), delimiter='\t'))

        assert problems == [], \
            'There is a problem with Record resource tsv'

class TestRecordResourceTtl(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.ttl' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/turtle', {'charset':'UTF-8'})

    def test_response_contents(self, response, endpoint, record_ttl_schema, register_domain):
        fieldNs = 'http://field.'+ register_domain +'/record/'
        specificationNs = 'https://openregister.github.io/specification/#'

        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['register-record']['fields']

        record_ttl_schema.add_data(response.text)
        record_ttl_schema.add_fields(fieldNs, register_fields)
        record_ttl_schema.addEntryFieldsToValidation(specificationNs)
        
        problems = record_ttl_schema.validateFieldsExist()
        problems += record_ttl_schema.validateDataMatchesFieldDataTypes(specificationNs)

        assert problems == [], \
            'There is a problem with Record resource ttl'

class RecordCsvSchema:
    def get_schema(self, endpoint):
        field_names = ['entry-number', 'entry-timestamp', 'item-hash']
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['register-record']['fields']
        field_names += register_fields

        validator = CSVValidator(field_names)
        validator.add_header_check()
        validator.add_value_check('entry-number', str, match_pattern('^\d+$'))
        validator.add_value_check('item-hash', str, match_pattern('^sha-256:[a-f\d]{64}$'))
        validator.add_value_check('entry-timestamp', str, match_pattern('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'))
        return validator