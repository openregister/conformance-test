import csv
import pytest
import requests
import re
import yaml

from csvvalidator import *
from urllib.parse import urljoin
from werkzeug.http import parse_options_header

class TestItemResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entry/1.json'))

        item_hash = entry.json()['item-hash']

        return requests.get(urljoin(endpoint, 'item/' + item_hash + '.json'))

    def test_response_contents(self, response, endpoint):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['record']['entry']['fields']

        assert set(response.json().keys()).issubset(register_fields), \
            'Item json does not match fields specified in regsiter register'

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

class TestItemResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entry/1.json'))

        item_hash = entry.json()['item-hash']

        return requests.get(urljoin(endpoint, 'item/' + item_hash + '.yaml'))

    def test_response_contents(self, response, endpoint):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['record']['entry']['fields']

        assert set(yaml.load(response.text).keys()).issubset(register_fields), \
            'Item json does not match fields specified in regsiter register'

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/yaml', {'charset':'UTF-8'})

class TestItemResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entry/1.json'))

        item_hash = entry.json()['item-hash']

        return requests.get(urljoin(endpoint, 'item/' + item_hash + '.csv'))

    def test_response_contents(self, response, endpoint):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['record']['entry']['fields']

        validator = CSVValidator(register_fields)
        validator.add_header_check()
        problems = validator.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Item resource csv'

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/csv', {'charset':'UTF-8'})