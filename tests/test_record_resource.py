import csv
import pytest
import requests
import yaml

import tests.data_types as types
from csvvalidator import *
from jsonschema import validate
from urllib.parse import urljoin
from werkzeug.http import parse_options_header


@pytest.mark.version(1)
class TestRecordResourceJsonV1(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'items/%s.json' % entry_json['item-hash'][0])).json()

        return item_json[register_name], requests.get(urljoin(endpoint, 'records/%s.json' % item_json[register_name]))

    def test_content_type(self, response):
        key, record_response = response
        assert record_response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, endpoint, record_schema_v1):
        key, record_response = response

        record_json = record_response.json()
        validate(record_json, record_schema_v1)

        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']

        assert set(record_json[key]['item'][0].keys()).issubset(register_fields), \
            'Record contains unrecognized keys'


@pytest.mark.version(2)
class TestRecordResourceJsonV2(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()
        blob_json = requests.get(urljoin(endpoint, 'blobs/%s.json' % entry_json['blob-hash'])).json()

        return blob_json[register_name], requests.get(urljoin(endpoint, 'records/%s.json' % blob_json[register_name]))

    def test_content_type(self, response):
        key, record_response = response
        assert record_response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, endpoint, record_schema_v2):
        key, record_response = response

        record_json = record_response.json()
        validate(record_json, record_schema_v2)

        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']

        assert set(record_json['blob'].keys()).issubset(register_fields), \
            'Record contains unrecognized keys'


@pytest.mark.version(1)
class TestRecordResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'items/%s.json' % entry_json['item-hash'][0])).json()

        return item_json[register_name], requests.get(urljoin(endpoint, 'records/%s.yaml' % item_json[register_name]))


    def test_content_type(self, response):
        key, record_response = response
        assert parse_options_header(record_response.headers['content-type']) \
               == ('text/yaml', {'charset': 'UTF-8'})

    @pytest.mark.xfail(reason="""yaml.load decodes some register keys as integers because we do not wrap our codes in apostrophes.
        This will fail for some registers and not others and might be a problem with our YAML representation.""")
    def test_response_contents(self, response, endpoint, record_schema_v1):
        key, record_response = response

        record_json = yaml.load(record_response.text)
        validate(record_json, record_schema_v1)

        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']

        item_field_names = record_json[key]['item'][0].keys()

        assert set(item_field_names).issubset(register_fields), \
            'Record contains unrecognized keys'


@pytest.mark.version(1)
class TestRecordResourceCsvV1(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'items/%s.json' % entry_json['item-hash'][0])).json()

        return requests.get(urljoin(endpoint, 'records/%s.csv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    def test_response_contents(self, response, endpoint):
        csv_schema = get_schema_v1(endpoint)
        problems = csv_schema.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Record resource csv'


@pytest.mark.version(2)
class TestRecordResourceCsvV2(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()
        item_json = requests.get(urljoin(endpoint, 'blobs/%s.json' % entry_json['blob-hash'])).json()

        return requests.get(urljoin(endpoint, 'records/%s.csv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    def test_response_contents(self, response, endpoint):
        csv_schema = get_schema_v2(endpoint)
        problems = csv_schema.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Record resource csv'


@pytest.mark.version(1)
class TestRecordResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'items/%s.json' % entry_json['item-hash'][0])).json()

        return requests.get(urljoin(endpoint, 'records/%s.tsv' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/tab-separated-values', {'charset': 'UTF-8'})

    def test_response_contents(self, response, endpoint):
        tsv_schema = get_schema_v1(endpoint)
        problems = tsv_schema.validate(csv.reader(response.text.split('\n'), delimiter='\t'))

        assert problems == [], \
            'There is a problem with Record resource tsv'


@pytest.mark.version(1)
class TestRecordResourceTtl(object):
    @pytest.fixture
    def response(self, endpoint, register):
        register_name = register
        entry_json = requests.get(urljoin(endpoint, 'entries/1.json')).json()[0]
        item_json = requests.get(urljoin(endpoint, 'items/%s.json' % entry_json['item-hash'][0])).json()

        return requests.get(urljoin(endpoint, 'records/%s.ttl' % item_json[register_name]))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/turtle', {'charset': 'UTF-8'})

    def test_response_contents(self, response, endpoint, record_ttl_schema, register_domain):
        field_namespace = 'http://field.%s/records/' % register_domain
        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']

        record_ttl_schema.add_data(response.text)
        record_ttl_schema.add_fields(field_namespace, register_fields)
        record_ttl_schema.add_entry_fields_to_validation()

        problems = record_ttl_schema.validate_fields_exist()
        problems += record_ttl_schema.validate_data_matches_field_data_types()

        assert problems == [], \
            'There is a problem with Record resource ttl'


def get_schema_v1(endpoint):
    field_names = ['index-entry-number','entry-number', 'entry-timestamp', 'key']
    register_data = requests.get(urljoin(endpoint, 'register.json'))
    register_fields = register_data.json()['register-record']['fields']
    field_names += register_fields

    validator = CSVValidator(field_names)
    validator.add_header_check()
    validator.add_value_check('index-entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('key', str, match_pattern(types.KEY_PATTERN))
    validator.add_value_check('entry-timestamp', str, match_pattern(types.TIMESTAMP_PATTERN))
    return validator


def get_schema_v2(endpoint):
    field_names = ['entry-number', 'entry-timestamp', 'key']
    register_data = requests.get(urljoin(endpoint, 'register.json'))
    register_fields = register_data.json()['register-record']['fields']
    field_names += register_fields

    validator = CSVValidator(field_names)
    validator.add_header_check()
    validator.add_value_check('entry-number', str, match_pattern(types.ENTRY_NUMBER_PATTERN))
    validator.add_value_check('key', str, match_pattern(types.KEY_PATTERN))
    validator.add_value_check('entry-timestamp', str, match_pattern(types.TIMESTAMP_PATTERN))
    return validator