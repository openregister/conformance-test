import pytest
import requests
import re

from urllib.parse import urljoin
from jsonschema import validate


class TestRecordResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s.json' % item_json[register_name]))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    def test_response_contents(self, response, endpoint, entry_schema):
        record_json = response.json()

        entry_part = {
            'entry-number': record_json.pop('entry-number'),
            'item-hash': record_json.pop('item-hash'),
            'entry-timestamp': record_json.pop('entry-timestamp')
        }

        validate(entry_part, entry_schema)

        register_data = requests.get(urljoin(endpoint, '/register.json'))

        register_fields = register_data.json()['record']['entry']['fields']

        assert set(record_json.keys()).issubset(register_fields), \
            'Record contains unrecognized keys'
