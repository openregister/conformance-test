import csv
import pytest
import requests
import multihash

from csvvalidator import *
from urllib.parse import urljoin
from werkzeug.http import parse_options_header
from jsonschema import validate


class ResourceTestBase:
    resource_type = ''

    @pytest.fixture
    def item_hash(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entries/1.json'))
        return entry.json()[0]['item-hash'][0]

    @pytest.fixture
    def blob_hash(self, endpoint):
        entry = requests.get(urljoin(endpoint, 'entries/1.json'))
        return entry.json()['blob-hash']

    @pytest.fixture
    def item_response(self, endpoint, item_hash):
        return requests.get(urljoin(endpoint, 'items/%s.%s' % (item_hash, self.resource_type)))

    @pytest.fixture
    def blob_response(self, endpoint, blob_hash):
        return requests.get(urljoin(endpoint, 'blobs/%s.%s' % (blob_hash, self.resource_type)))

    @pytest.fixture
    def register_fields(self, endpoint):
        register_data = requests.get(urljoin(endpoint, 'register.json'))
        return register_data.json()['register-record']['fields']


@pytest.mark.version(1)
class TestItemResourceJsonV1(ResourceTestBase):
    resource_type = 'json'

    def test_response_contents(self, item_response, endpoint):
        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']

        assert set(item_response.json().keys()).issubset(register_fields), \
            'Item json does not match fields specified in register register'

    def test_content_type(self, item_response):
        assert item_response.headers['content-type'] == 'application/json'


@pytest.mark.version(2)
class TestItemResourceJsonV2(ResourceTestBase):
    resource_type = 'json'

    def test_response_contents(self, blob_response, blob_schema, endpoint):
        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']

        blob = blob_response.json()
        blob_keys = set(blob.keys() - ['_id'])
        validate(blob, blob_schema)

        assert blob_keys.issubset(register_fields), 'Blob json does not match fields specified in the register definition'

    def test_content_type(self, blob_response):
        assert blob_response.headers['content-type'] == 'application/json'

    def test_hash_format(self, blob_response, endpoint):
        blob = blob_response.json()
        blob_id = blob['_id']
        assert multihash.is_valid(bytes.fromhex(blob_id))


@pytest.mark.version(1)
class TestItemResourceCsv(ResourceTestBase):
    resource_type = 'csv'

    def test_response_contents(self, item_response, endpoint, register_fields):
        csv_schema = CSVValidator(register_fields)
        csv_schema.add_header_check()
        problems = csv_schema.validate(csv.reader(item_response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Item resource csv'

    def test_content_type(self, item_response):
        assert parse_options_header(item_response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})


@pytest.mark.version(2)
class TestItemResourceCsv(ResourceTestBase):
    resource_type = 'csv'

    def test_response_contents(self, blob_response, register_fields, endpoint):
        response = requests.get(urljoin(endpoint, 'blobs.csv'))

        validator = CSVValidator(['_id'] + register_fields)
        validator.add_header_check()

        problems = validator.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], '/blobs CSV fields do not match the register definition'

    def test_content_type(self, blob_response):
        assert parse_options_header(blob_response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})

    def test_hash_format(self, endpoint, blob_response):
        reader = csv.DictReader((line.decode('utf8') for line in blob_response.iter_lines()))

        for blob in reader:
            blob_id = blob['_id']
            assert multihash.is_valid(bytes.fromhex(blob_id))