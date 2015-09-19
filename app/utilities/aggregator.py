""" This module interfaces with GitHub. """


from os.path import splitext
from json import loads
from base64 import b64decode
from requests import get
from .murls import https


VALID_EXTENSIONS = ('.ipynb', '.md')


class PostAggregationFailed(Exception):
    pass


class Aggregator(object):
    """ The Aggregator class helps collecting files from a repository. """

    def __init__(self, repo=None, exclude=(), token=None, user=None, branch='master'):
        assert repo and user, 'The aggregator needs at least a repository and a user'

        self.token = token
        self.user = user
        self.branch = branch
        self.repo = repo
        self.exclude = exclude

        self.base_url = https('api.github.com').query(access_token=self.token)

    @staticmethod
    def request_json(url):
        response = get(url=url, headers={'User-Agent': 'Aligator the Aggregator'})

        if response.status_code == 200:
            json = loads(response.text)
            return json
        else:
            raise PostAggregationFailed('The GitHub API responded with %s' % response.status_code)

    def get_repo(self):
        """ Return the hash of the specified branch of the repository. """
        url = self.base_url.path('repos',
                                 self.user,
                                 self.repo,
                                 'branches',
                                 self.branch)

        json = self.request_json(url)
        return json['commit']['sha']

    def get_files_in_repo(self, repo_hash):
        """ Return the hashes of all the files in the repository. """
        url = self.base_url.path('repos',
                                 self.user,
                                 self.repo,
                                 'git',
                                 'trees',
                                 repo_hash)

        json = self.request_json(url)

        for file in json['tree']:
            filename = file['path']
            extension = splitext(filename)[1]

            if filename not in self.exclude:
                if extension in VALID_EXTENSIONS:
                    yield file['sha'], file['path']

    def get_file_content(self, file_hash):
        """ Return the content of a file as unicode. """
        url = self.base_url.path('repos',
                                 self.user,
                                 self.repo,
                                 'git',
                                 'blobs',
                                 file_hash)

        json = self.request_json(url)

        content_as_bytes = b64decode(json['content'])
        content_as_unicode = content_as_bytes.decode()

        return content_as_unicode

    def get_file_commit(self, filename):
        """ Return the author, the date and the message of the last file commit. """
        url = self.base_url.path('repos',
                                 self.user,
                                 self.repo,
                                 'commits').query(file=filename)

        json = self.request_json(url)

        last = json[0]['commit']
        return last['author']['name'], last['author']['date'], last['message']


def fetch_posts(**kwargs):
    """ Fetch the posts from the repository. """
    a = Aggregator(**kwargs)

    try:
        repo = a.get_repo()
        files = a.get_files_in_repo(repo)

        for sha, filename in files:
            content = a.get_file_content(sha)
            author, date, message = a.get_file_commit(filename)

            yield filename, author, date, message, content

    except PostAggregationFailed:
        raise


if __name__ == '__main__':
    pass
