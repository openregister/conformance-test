import pytest
import requests
import re

from urllib.parse import urljoin


class TestItemResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        self.endpoint = endpoint

        self.register_name = re.sub(r'http[s]?://([^\.]+)(.*)', r'\1', endpoint)

        self.register_register_endpoint = re.sub(r'(http[s]?://)([^\.]+)(.*)', r'\1register\3', endpoint)

        entry = requests.get(urljoin(endpoint, 'entry/1.json'))

        item_hash = entry.json()['item-hash']

        return requests.get(urljoin(endpoint, 'item/' + item_hash + '.json'))

    @pytest.mark.xfail
    def test_response_contents(self, response):
        register_data = requests.get(
            urljoin(self.endpoint, self.register_register_endpoint + '/register/' + self.register_name + '.json'))

        register_fields = register_data.json()['fields']

        assert set(response.json().keys()).issubset(register_fields), \
            'Item json does not match fields specified in regsiter register'
