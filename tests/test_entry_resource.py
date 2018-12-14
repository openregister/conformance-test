import csv
import pytest
import requests
import multihash

from jsonschema import validate
from urllib.parse import urljoin
from werkzeug.http import parse_options_header


class TestEntryResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries/1.json'))

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    @pytest.mark.version(1)
    def test_response_contents(self, response, entry_schema_v1):
        validate(response.json(), entry_schema_v1)

    @pytest.mark.version(2)
    def test_response_contents(self, response, entry_schema_v2):
        validate(response.json(), entry_schema_v2)

    @pytest.mark.version(2)
    def test_hash_format(self, response):
        entry = response.json()
        blob_hash = entry['blob-hash']
        assert multihash.is_valid(bytes.fromhex(blob_hash))


class TestEntryResourceCsv(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entries/1.csv'))

    @pytest.mark.version(1)
    @pytest.mark.version(2)
    def test_content_type(self, response):
        assert parse_options_header(response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    @pytest.mark.version(1)
    def test_response_contents(self, response, entry_csv_schema_v1):
        problems = entry_csv_schema_v1.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Entry resource csv'

    @pytest.mark.version(2)
    def test_response_contents(self, response, entry_csv_schema_v2):
        problems = entry_csv_schema_v2.validate(csv.reader(response.text.split('\r\n')))
        assert problems == [], \
            'There is a problem with Entry resource csv'

    @pytest.mark.version(2)
    def test_hash_format(self, response):
        reader = csv.DictReader((line.decode('utf8') for line in response.iter_lines()))

        for entry in reader:
            blob_hash = entry['blob-hash']
            assert multihash.is_valid(bytes.fromhex(blob_hash))