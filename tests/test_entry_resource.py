import csv
import pytest
import requests
import yaml
import rdflib
import re

from jsonschema import validate
from urllib.parse import urljoin
from werkzeug.http import parse_options_header
from rdflib.graph import Graph
from rdflib.namespace import Namespace

class TestEntryResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, entry_schema):
        validate(response.json(), entry_schema)

class TestEntryResourceYaml(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.yaml'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/yaml', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_schema):
        validate(yaml.load(response.text), entry_schema)

class TestEntryResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.csv'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/csv', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema):
        problems = entry_csv_schema.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Entry resource csv'

class TestEntryResourceTsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.tsv'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/tab-separated-values', {'charset':'UTF-8'})

    def test_response_contents(self, response, entry_csv_schema):
        problems = entry_csv_schema.validate(csv.reader(response.text.split('\n'), delimiter='\t'))
        assert problems == [], \
            'There is a problem with Entry resource tsv'

class TestEntryResourceTtl(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.ttl'))

    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
            == ('text/turtle', {'charset':'UTF-8'})

    def test_response_contents(self, response, entries_schema):
        graph = Graph()
        graph.parse(data=response.text, format="turtle")

        specification = Namespace('https://openregister.github.io/specification/#')

        predicateRegexMap = {
            "entry-number-field": re.compile('^\d+$'),
            "entry-timestamp-field": re.compile('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'),
            "item-resource": re.compile('/item/sha-256:[a-f\d]{64}$'),
            "key-field": re.compile('.+')
        }

        problems = []

        for p, r in predicateRegexMap.items():
            objects = list(graph.objects(subject=None, predicate=specification[p]))
            problems.extend(v for k, v in enumerate(objects) if r.search(v) is None)

        assert problems == [], \
            'There is a problem with Entry resource ttl'

