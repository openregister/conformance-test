import pytest
import requests
import re

from urllib.parse import urljoin


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
