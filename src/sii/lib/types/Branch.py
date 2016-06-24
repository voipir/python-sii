""" Static Company Branch Data (coming from YAML)

For a Template example look into files/companies.yml at the root of the repository.
"""


class Branch(object):

    def __init__(self, yml):
        self.__dict__.update(yml)

    def __getattr__(self, key):
        if key in self.__dict__:
            return super().__getattr__(key)
        else:
            raise RuntimeError("Expected and did not find <{0}> in branch section of YAML.".format(key))
