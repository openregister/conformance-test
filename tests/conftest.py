import pytest


def pytest_addoption(parser):
    parser.addoption("--endpoint", action="append",
        help="register endpoints to test")


def pytest_generate_tests(metafunc):
    if 'endpoint' in metafunc.fixturenames:
        metafunc.parametrize("endpoint",
            metafunc.config.option.endpoint)
