""" This module aggregates content from other websites. """


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
        if app.debug:
            pprint(json)

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
        if app.debug:
            pprint(json)

        for file in json['tree']:
            if file['path'] not in self.exclude:
                yield file['sha'], file['path']

    def get_file_content(self, file_hash):
        """ Return the content of a post as unicode. """

        url = self.url.path('repos',
                            self.user,
                            self.repo,
                            'git',
                            'blobs',
                            file_hash)

        json = self.request_json(url)

        content = b64decode(json['content']).decode()
        if app.debug:
            print(content)

        return content

    def get_last_commit(self, filename):
        """ Return the author, the date and the message of the last commit made to a file. """

        json = self.request_json(self.url.path('repos',
                                               self.user,
                                               self.repo,
                                               'commits').query(file=filename))

        last = json[0]['commit']
        if app.debug:
            pprint(json)

        return last['author']['name'], last['author']['date'], last['message']

if __name__ == '__main__':
    """ Demonstrate the use of the module. """

    app.debug = False
    pa = Aggregator()
    repo_ = pa.get_repo_hash()
    files = pa.get_file_hashes(repo_)

    for sha, file_ in files:
        text = pa.get_file_content(sha)
        author, date, message = pa.get_last_commit(file_)
        print(file_, author, date, message)
