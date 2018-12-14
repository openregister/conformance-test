import csv
import pytest
import requests
import warnings

from csvvalidator import CSVValidator
from urllib.parse import urljoin
from jsonschema import validate
from multihash import multihash

@pytest.fixture
def register_fields(endpoint):
    '''
    Ask the register for its fields
    TODO: this will be superseded by the context endpoint in V2
    '''
    register_data = requests.get(urljoin(endpoint, 'register.json'))
    return register_data.json()['register-record']['fields']


@pytest.mark.version(2)
class TestBlobsResourceJSON:
    def test_response_contents(self, register_fields, blobs_schema, endpoint):
        response = requests.get(urljoin(endpoint, 'blobs'))
        parsed_response = response.json()

        validate(parsed_response, blobs_schema)

        if not parsed_response:
            warnings.warn('Some checks were skipped because the register contains no blobs.', warnings.RuntimeWarning)

        for blob in parsed_response:
            blob_keys = set(blob.keys() - ['_id'])
            assert blob_keys.issubset(register_fields), 'Blob json does not match fields specified in the register definition'

    def test_hash_format(self, endpoint):
        response = requests.get(urljoin(endpoint, 'blobs'))
        parsed_response = response.json()

        for blob in parsed_response:
            blob_id = blob['_id']
            assert multihash.is_valid(bytes.fromhex(blob_id))

    def test_content_type(self, endpoint):
        response = requests.get(urljoin(endpoint, 'blobs'))

        assert response.headers['content-type'] == 'application/json'


@pytest.mark.version(2)
class TestBlobsResourceCSV:
    def test_response_contents(self, register_fields, endpoint):
        response = requests.get(urljoin(endpoint, 'blobs.csv'))

        validator = CSVValidator(['_id'] + register_fields)
        validator.add_header_check()

        problems = validator.validate(csv.reader(response.text.split('\r\n')))

        assert problems == [], '/blobs CSV fields do not match the register definition'

    def test_hash_format(self, endpoint):
        response = requests.get(urljoin(endpoint, 'blobs.csv'))
        reader = csv.DictReader((line.decode('utf8') for line in response.iter_lines()))

        for blob in reader:
            blob_id = blob['_id']
            assert multihash.is_valid(bytes.fromhex(blob_id))

    def test_content_type(self, endpoint):
        response = requests.get(urljoin(endpoint, 'blobs.csv'))

        assert response.headers['content-type'] == 'text/csv;charset=UTF-8'