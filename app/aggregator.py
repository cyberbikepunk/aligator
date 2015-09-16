""" This module aggregates content from other websites. """

import sys
from pprint import pprint

pprint(sys.path)

from requests import get
from json import loads
from base64 import b64decode
from ..blog import app

from .murls import https
from instance.config import TOKEN, USER, REPO, BRANCH, EXCLUDE


class Aggregator(object):
    url = https('api.github.com')

    def __init__(self, token=TOKEN, user=USER, repo=REPO, branch=BRANCH, exclude=EXCLUDE):
        self.token = token
        self.user = user
        self.branch = branch
        self.repo = repo
        self.exclude = exclude

    def request_json(self, url):
        response = get(url=url, params={'token': self.token})

        if response.status_code == 200:
            json = loads(response.text)
            return json
        else:
            app.logger.error('%s failed with %s ', response.url, response.status_code)

    def get_repo_hash(self):
        """ Return the hash of the master branch of the posts repo. """

        repo_url = self.url.path('repos',
                                 self.user,
                                 self.repo,
                                 'branches',
                                 self.branch)

        json = self.request_json(repo_url)
        return json['commit']['sha']

    def get_file_hashes(self, repo_hash):
        """ Return the hashes of all posts found inside the repo. """

        tree_url = self.url.path('repos',
                                 self.user,
                                 self.repo,
                                 'git',
                                 'trees',
                                 repo_hash)

        json = self.request_json(tree_url)

        for file in json['tree']:
            if file['path'] not in self.exclude:
                yield file['sha']

    def get_file_content(self, file_hash):
        """ Return the content of a post as unicode. """

        url = self.url.path('repos',
                            self.user,
                            self.repo,
                            'git',
                            'blobs',
                            file_hash)

        json = self.request_json(url)
        content = b64decode(json['content'])
        return content.decode()


if __name__ == '__main__':
    """ Demonstrate the use of the module. """

    pa = Aggregator()
    repo_ = pa.get_repo_hash()
    files = pa.get_file_hashes(repo_)

    for file_id in files:
        text = pa.get_file_content(file_id)
        print(text)
