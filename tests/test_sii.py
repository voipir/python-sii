""" Test Interactions with the SII Servers

This tests require the following arguments passed to the test executable ./test.py:

    --key-path  path/to/key/file.pem
    --cert-path path/to/certificate/file.crt
"""
from sii.server.ptcl import Seed, Token  # , Authentication


def test_palena_auth_seed():
    s = Seed("https://palena.sii.cl/DTEWS/CrSeed.jws?wsdl")
    assert not s.message


def test_palena_auth_token(key_path, cert_path):
    s = Seed("https://palena.sii.cl/DTEWS/CrSeed.jws?wsdl")
    t = Token(s, key_path, cert_path, "https://palena.sii.cl/DTEWS/GetTokenFromSeed.jws?wsdl")
    assert t.message == "Token Creado"


def test_maullin_auth_seed():
    s = Seed("https://maullin.sii.cl/DTEWS/CrSeed.jws?wsdl")
    assert not s.message


def test_maullin_auth_token(key_path, cert_path):
    s = Seed("https://maullin.sii.cl/DTEWS/CrSeed.jws?wsdl")
    t = Token(s, key_path, cert_path, "https://maullin.sii.cl/DTEWS/GetTokenFromSeed.jws?wsdl")
    assert t.message == "Token Creado"
