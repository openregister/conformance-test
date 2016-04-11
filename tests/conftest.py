import pytest


def pytest_addoption(parser):
    parser.addoption("--endpoint", action="append",
        help="register endpoints to test")


def pytest_generate_tests(metafunc):
    if 'endpoint' in metafunc.fixturenames:
        metafunc.parametrize("endpoint",
            metafunc.config.option.endpoint)


@pytest.fixture(scope="session")
def entry_schema():
    # This schema should always represent the response json specified at <http://openregister.github.io/specification/#entry-resource>
    return {
        "type": "object",
        "properties": {
            "entry-number": {
                "type": "string",
                "pattern": "^\d+$"
            },
            "item-hash": {
                "type": "string",
                "pattern": "^sha-256:[a-f\d]{64}$"
            },
            "entry-timestamp": {
                "type": "string",
                "pattern": "^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
            }
        },
        "required": ["entry-number", "item-hash", "entry-timestamp"],
        "additionalProperties": False
    }

