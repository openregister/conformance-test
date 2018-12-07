import csv
import pytest
import requests

import tests.data_types as types
from csvvalidator import *
from jsonschema import validate
from urllib.parse import urljoin
from werkzeug.http import parse_options_header
from .test_record_resource import get_schema_v2


@pytest.mark.version(2)
class TestRecordsResourceJsonV2(object):
    @pytest.fixture
    def response(self, endpoint, register):
        return requests.get(urljoin(endpoint, 'records.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, endpoint, records_schema_v2):
        records_json = response.json()
        validate(records_json, records_schema_v2)

        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']
        assert all(
            set(record_json.keys() - ['_id']).issubset(register_fields)
            for record_json in records_json
        )
        assert all(
            '_id' in record_json
            for record_json in records_json
        ),\
                 'Record contains unrecognized keys'


@pytest.mark.version(2)
class TestRecordsResourceCsvV2(object):
    @pytest.fixture
    def response(self, endpoint, register):

        return requests.get(urljoin(endpoint, 'records.csv'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    def test_response_contents(self, response, endpoint):
        csv_schema = get_schema_v2(endpoint)
        problems = csv_schema.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Record resource csv'