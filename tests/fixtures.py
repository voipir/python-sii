"""
"""
import pytest


def pytest_addoption(parser):
    parser.addoption("--key-path", action="store", dest="key_path",
                     help="Provide private Key to authenticate at SII Servers")
    parser.addoption("--cert-path", action="store", dest="cert_path",
                     help="Provide certificate to authenticate at SII Servers")


@pytest.fixture(scope='session')
def key_path(request):
    return request.config.option.key_path


@pytest.fixture(scope='session')
def cert_path(request):
    return request.config.option.cert_path
