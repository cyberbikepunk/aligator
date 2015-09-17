""" Miscellaneous utilities. """

from yaml import safe_load
from os.path import abspath, dirname, join
from pprint import pprint


def get_blog_settings():
    user_settings = abspath(join(dirname(__file__), '..', '..', 'instance', 'user.yml'))

    with open(user_settings) as f:
        yaml = f.read()
        return safe_load(yaml)


if __name__ == '__main__':
    settings = get_blog_settings()
    pprint(settings)
