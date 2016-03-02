import pytest
import requests
from urllib.parse import urljoin


class TestRegisterResourceJson(object):
    @pytest.fixture
    def response(self, endpoint):
        return requests.get(urljoin(endpoint, 'entry/1.json'))

    def test_content_type(self, response):
        assert response.headers['content-type'] == 'application/json'

    @pytest.mark.xfail
    def test_content_fieldnames(self, response):
        assert 'entry-number' in response.json(), \
            '''Missing required field `entry-number`
            Ref: http://openregister.github.io/specification/#entry-resource'''
