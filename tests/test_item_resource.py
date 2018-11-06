import csv
import pytest
import requests
import yaml

from csvvalidator import *
from urllib.parse import urljoin
from werkzeug.http import parse_options_header


class ResourceTestBase(object):
    resource_type = ''

    @pytest.fixture(autouse=True)
    def response(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entry/1.json'))
        item_hash = entry.json()[0]['item-hash'][0]

        return requests.get(urljoin(endpoint, 'item/%s.%s' % (item_hash, self.resource_type)))

    def get_schema(self, endpoint):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['register-record']['fields']

        validator = CSVValidator(register_fields)
        validator.add_header_check()
        return validator


class TestItemResourceJson(ResourceTestBase):
    resource_type = 'json'

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_response_contents(self, response, endpoint):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['register-record']['fields']

        assert set(response.json().keys()).issubset(register_fields), \
            'Item json does not match fields specified in register register'

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'


class TestItemResourceYaml(ResourceTestBase):
    resource_type = 'yaml'

    @pytest.mark.version(1)
    def test_response_contents(self, response, endpoint):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['register-record']['fields']

        assert set(yaml.load(response.text).keys()).issubset(register_fields), \
            'Item json does not match fields specified in register register'

    @pytest.mark.version(1)
    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/yaml', {'charset': 'UTF-8'})


class TestItemResourceCsv(ResourceTestBase):
    resource_type = 'csv'

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_response_contents(self, response, endpoint):
        csv_schema = self.get_schema(endpoint)
        problems = csv_schema.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Item resource csv'

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})


class TestItemResourceTsv(ResourceTestBase):
    resource_type = 'tsv'

    @pytest.mark.version(1)
    def test_response_contents(self, response, endpoint):
        tsv_schema = self.get_schema(endpoint)
        problems = tsv_schema.validate(csv.reader(response.text.split('\n'), delimiter='\t'))

        assert problems == [], \
            'There is a problem with Item resource tsv'

    @pytest.mark.version(1)
    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/tab-separated-values', {'charset': 'UTF-8'})


class TestItemResourceTtl(ResourceTestBase):
    resource_type = 'ttl'

    @pytest.mark.version(1)
    def test_response_contents(self, response, endpoint, entry_ttl_schema, register_domain):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['register-record']['fields']
        namespace = 'http://field.%s/records/' % register_domain

        entry_ttl_schema.add_data(response.text)
        entry_ttl_schema.add_fields(namespace, register_fields)
        entry_ttl_schema.add_entry_fields_to_validation()

        problems = entry_ttl_schema.validate_fields_exist()
        problems += entry_ttl_schema.validate_data_matches_field_data_types()

        assert problems == [], \
            'There is a problem with Item resource ttl'

    @pytest.mark.version(1)
    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/turtle', {'charset': 'UTF-8'})
