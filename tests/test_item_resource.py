import pytest
import requests
import re

from urllib.parse import urljoin


class TestItemResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        self.register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        entry = requests.get(urljoin(endpoint, 'entry/1.json'))

        item_hash = entry.json()['item-hash']

        return requests.get(urljoin(endpoint, 'item/' + item_hash + '.json'))

    def test_response_contents(self, response, register_register_endpoint ):
        register_data = requests.get(
            urljoin(register_register_endpoint, '/record/' + self.register_name + '.json'))

        register_fields = register_data.json()['fields']

        assert set(response.json().keys()).issubset(register_fields), \
            'Item json does not match fields specified in regsiter register'


    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'
