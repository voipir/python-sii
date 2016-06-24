""" Company Pool to resolve Company objects from (coming from YAML)

For a Template example look into files/companies.yml at the root of the repository. Such a file can
hold more than one instances of company metadata inside, allowing for multiple companies being
handled transparently by the same library or client/server application.
"""
import io

import yaml

from sii.lib.lib import fileio

from .Company import Company
from .Branch  import Branch


class CompanyPool(object):

    def __init__(self, yml):
        self._companies = {}

        for rut, data in yml.items():
            self._companies[rut] = Company(data)

    def __getitem__(self, key):
        company = self._companies.get(key, None)

        if company is None:
            raise KeyError("Expected and did not find company with RUT: <{0}> in YAML.".format(key))

        return company

    @classmethod
    def from_file(cls, path):
        buff = io.StringIO(fileio.read(path))
        yml  = yaml.load(buff)

        return cls(yml)
