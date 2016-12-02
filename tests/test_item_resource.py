import csv
import pytest
import requests
import yaml
import rdflib
import re

from csvvalidator import *
from urllib.parse import urljoin
from werkzeug.http import parse_options_header
from rdflib.graph import Graph
from rdflib.namespace import Namespace

class TestItemResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entry/1.json'))
        item_hash = entry.json()['item-hash']

        return requests.get(urljoin(endpoint, 'item/' + item_hash + '.json'))

    def test_response_contents(self, response, endpoint):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['register-record']['fields']

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
        register_fields = register_data.json()['register-record']['fields']

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
        csvSchema = RecordCsvSchema.get_schema(self, endpoint)
        problems = csvSchema.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Item resource csv'

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/csv', {'charset':'UTF-8'})

class TestItemResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entry/1.json'))
        item_hash = entry.json()['item-hash']

        return requests.get(urljoin(endpoint, 'item/' + item_hash + '.tsv'))

    def test_response_contents(self, response, endpoint):
        tsvSchema = RecordCsvSchema.get_schema(self, endpoint)
        problems = tsvSchema.validate(csv.reader(response.text.split('\n'), delimiter='\t'))

        assert problems == [], \
            'There is a problem with Item resource tsv'

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/tab-separated-values', {'charset':'UTF-8'})

class TestItemResourceTtl(object):
    @pytest.fixture
    def response(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entry/1.json'))
        item_hash = entry.json()['item-hash']

        return requests.get(urljoin(endpoint, 'item/' + item_hash + '.ttl'))

    def test_response_contents(self, response, endpoint):
        graph = Graph()
        graph.parse(data=response.text, format="turtle")

        specification = Namespace('http://field.openregister.dev:8080/record/')

        # Get expected fields
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = [specification[f] for f in register_data.json()['register-record']['fields']]

        actualFields = list(graph.predicates())

        problems = []
        problems.extend(p for p in graph.predicates() if p not in register_fields)

        assert problems == [], \
            'There is a problem with Item resource ttl'

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/turtle', {'charset':'UTF-8'})

class RecordCsvSchema:
    def get_schema(self, endpoint):
        register_data = requests.get(urljoin(endpoint, '/register.json'))
        register_fields = register_data.json()['register-record']['fields']

        validator = CSVValidator(register_fields)
        validator.add_header_check()
        return validator