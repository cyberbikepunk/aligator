""" This module populates the blog from GitHub. """

from json import loads
from base64 import b64decode
from requests import get
from manage import app
from .murls import https
from .tools import get_blog_settings


class PostAggregatorException(Exception):
    pass


def aggregate():
    """ Fetch the posts from the repository. """

    a = Aggregator()

    try:
        repo = a.get_repo_hash()
        files = a.get_file_hashes(repo)

        for sha, file in files:
            text = a.get_file_content(sha)
            author, date, message = a.get_last_commit(file)

            yield file, author, date, message, text

    except PostAggregatorException:
        raise


class Aggregator(object):
    """ The Aggregator class queries the GitHub API. """

    def __init__(self):
        settings = get_blog_settings()

        self.url = https('api.github.com')
        self.token = settings['github']['token']
        self.user = settings['github']['user']
        self.branch = settings['github']['branch']
        self.repo = settings['github']['repo']
        self.exclude = settings['github']['exclude']

    def request_json(self, url):
        response = get(url=url, params={'token': self.token})

        if response.status_code == 200:
            json = loads(response.text)
            return json
        else:
            app.logger.error('Request to %s failed with %s ', response.url, response.status_code)
            raise PostAggregatorException('The GitHub API responded with %s' % response.status_code)

    def get_repo_hash(self):
        """ Return the hash of the master branch of the posts repo. """
        json = self.request_json(self.url.path('repos',
                                               self.user,
                                               self.repo,
                                               'branches',
                                               self.branch))
        return json['commit']['sha']

    def get_file_hashes(self, repo_hash):
        """ Return the hashes of all posts found inside the repo. """
        json = self.request_json(self.url.path('repos',
                                               self.user,
                                               self.repo,
                                               'git',
                                               'trees',
                                               repo_hash))
        for file in json['tree']:
            if file['path'] not in self.exclude:
                yield file['sha'], file['path']

    def get_file_content(self, file_hash):
        """ Return the content of a post as unicode. """
        json = self.request_json(self.url.path('repos',
                                               self.user,
                                               self.repo,
                                               'git',
                                               'blobs',
                                               file_hash))

        content_as_bytes = b64decode(json['content'])
        content_as_unicode = content_as_bytes.decode()

        return content_as_unicode

    def get_last_commit(self, filename):
        """ Return the author, the date and the message of the last file commit. """
        json = self.request_json(self.url.path('repos',
                                               self.user,
                                               self.repo,
                                               'commits').query(file=filename))
        last = json[0]['commit']
        return last['author']['name'], last['author']['date'], last['message']

if __name__ == '__main__':
    """ Demonstrate the use of the module. """

    for post in aggregate():
        for info in post:
            print(info)
