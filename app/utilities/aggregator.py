""" This module populates the blog from GitHub. """


from os.path import splitext
from json import loads
from base64 import b64decode
from requests import get
from app.utilities.murls import https
from instance.settings import GITHUB_REPO, GITHUB_EXCLUDE, GITHUB_TOKEN, GITHUB_USER, GITHUB_BRANCH


VALID_EXTENSIONS = ('.ipynb', '.md')


class PostAggregationFailed(Exception):
    pass


class Aggregator(object):
    """ The Aggregator class queries the GitHub API. """

    def __init__(self):
        self.url = https('api.github.com')

        self.token = GITHUB_TOKEN
        self.user = GITHUB_USER
        self.branch = GITHUB_BRANCH
        self.repo = GITHUB_REPO
        self.exclude = GITHUB_EXCLUDE

    @staticmethod
    def request_json(url):
        response = get(url=url,
                       params={'access_token': GITHUB_TOKEN},
                       headers={'User-Agent': 'Aligator the Aggregator'})

        if response.status_code == 200:
            json = loads(response.text)
            return json
        else:
            raise PostAggregationFailed('The GitHub API responded with %s' % response.status_code)

    def get_repo(self):
        """ Return the hash of the specified branch in the posts repository. """
        json = self.request_json(self.url.path('repos',
                                               self.user,
                                               self.repo,
                                               'branches',
                                               self.branch))
        return json['commit']['sha']

    def get_files_in_repo(self, repo_hash):
        """ Return the hashes of alget_repo_branchl posts found inside the repository. """
        json = self.request_json(self.url.path('repos',
                                               self.user,
                                               self.repo,
                                               'git',
                                               'trees',
                                               repo_hash))
        for file in json['tree']:
            filename = file['path']
            extension = splitext(filename)[1]

            if filename not in self.exclude:
                if extension in VALID_EXTENSIONS:
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

    def get_file_commit(self, filename):
        """ Return the author, the date and the message of the last file commit. """
        json = self.request_json(self.url.path('repos',
                                               self.user,
                                               self.repo,
                                               'commits').query(file=filename))
        last = json[0]['commit']
        return last['author']['name'], last['author']['date'], last['message']


def fetch_posts():
    """ Fetch the posts from the repository. """
    a = Aggregator()

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
