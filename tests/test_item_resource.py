import csv
import pytest
import requests

from csvvalidator import *
from urllib.parse import urljoin
from werkzeug.http import parse_options_header


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

    def get_schema(self, endpoint):
        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']

        validator = CSVValidator(register_fields)
        validator.add_header_check()
        return validator


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

    def test_response_contents(self, blob_response, endpoint):
        register_data = requests.get(urljoin(endpoint, 'register.json'))
        register_fields = register_data.json()['register-record']['fields']

        assert set(blob_response.json().keys()).issubset(register_fields), \
            'Item json does not match fields specified in register register'

    def test_content_type(self, blob_response):
        assert blob_response.headers['content-type'] == 'application/json'


@pytest.mark.version(1)
class TestItemResourceCsv(ResourceTestBase):
    resource_type = 'csv'

    def test_response_contents(self, item_response, endpoint):
        csv_schema = self.get_schema(endpoint)
        problems = csv_schema.validate(csv.reader(item_response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Item resource csv'

    def test_content_type(self, item_response):
        assert parse_options_header(item_response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})


@pytest.mark.version(2)
class TestItemResourceCsv(ResourceTestBase):
    resource_type = 'csv'

    def test_response_contents(self, blob_response, endpoint):
        csv_schema = self.get_schema(endpoint)
        problems = csv_schema.validate(csv.reader(blob_response.text.split('\r\n')))

        assert problems == [], \
            'There is a problem with Item resource csv'

    def test_content_type(self, blob_response):
        assert parse_options_header(blob_response.headers['content-type']) \
               == ('text/csv', {'charset': 'UTF-8'})