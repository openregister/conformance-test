import pytest
import requests
import re

from urllib.parse import urljoin
from jsonschema import validate

class TestRecordEntriesResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry_json = requests.get(urljoin(endpoint, 'entry/1.json')).json()

        item_json = requests.get(urljoin(endpoint, 'item/%s.json' % entry_json['item-hash'])).json()

        return requests.get(urljoin(endpoint, '/record/%s/entries' % item_json[register_name]))

    @pytest.mark.xfail
    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    @pytest.mark.xfail
    def test_response_contents(self, response, entries_schema):
        validate(response.json(), entries_schema)
