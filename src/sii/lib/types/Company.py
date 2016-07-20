""" Static Company Data (coming from YAML)

For a Template example look into files/companies.yml at the root of the repository.
"""
from .Branch import Branch


class Company(object):

    def __init__(self, data):
        self.__dict__.update(data)
        self.branches = [Branch(b) for b in self.branches]

    def __getattr__(self, key):
        if key in self.__dict__:
            return super().__getattr__(key)
        else:
            raise RuntimeError("Expected and did not find <{0}> in company YAML.".format(key))
