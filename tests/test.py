"""
"""
import sys
import pytest
import fixtures


def main():
    plugins = [fixtures]
    print(sys.argv)
    pytest.main(sys.argv[1:], plugins=plugins)


if __name__ == "__main__":
    main()
