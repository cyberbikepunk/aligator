""" This module collects posts on GitHub using the API. """


from base64 import b64decode
from os.path import splitext
from requests import Session
from werkzeug.utils import cached_property
from logging import error, debug

from logger import get_custom_logger
log = get_custom_logger(__name__)
log.info('hello')


class GitHubRequestError(Exception):
    blueprint = 'Requested {url}, got {code}: {json}'

    def __init__(self, response):
        message = self.blueprint.format(
            **{'code': response.status_code,
               'json': response.json(),
               'url': response.url}
        )
        error(message)
        super(GitHubRequestError, self).__init__(message)


class PostAggregator(object):
    """ This class collects posts from a GitHub repository. """

    GITHUB_API_URL = 'https://api.github.com/'
    VALID_EXTENSIONS = '.ipynb', '.md'

    def __init__(self,
                 repo=None,
                 exclude=(),
                 username=None,
                 password=None,
                 branch='master'):

        self.repo = repo
        self.branch = branch
        self.exclude = exclude
        self.user = username
        self.session = Session()
        self.session.auth = (username, password)

    def request(self, *path):
        url = self.GITHUB_API_URL + '/'.join(path)
        response = self.session.get(url=url)
        if response.status_code == 200:
            return response.json()
        else:
            raise GitHubRequestError(response)

    def collect_posts(self):
        branch_hash = self.request(
                'repos',
                self.user,
                self.repo,
                'branches',
                self.branch
        )['commit']['sha']
        files = self.request(
                'repos',
                self.user,
                self.repo,
                'git',
                'trees',
                branch_hash
        )['tree']
        for file in files:
            filename = file['path']
            extension = splitext(filename)[1]
            if filename not in self.exclude and extension in self.VALID_EXTENSIONS:
                debug('Found %s', filename)
                yield file['sha'], filename
            else:
                debug('Skipped %s', filename)

    def fetch_post_content(self, sha, filename):
        content = self.request(
                'repos',
                self.user,
                self.repo,
                'git',
                'blobs',
                sha
        )['content']
        content_as_bytes = b64decode(content)
        content_as_unicode = content_as_bytes.decode()
        debug('Extracted content for %s', filename)
        return content_as_unicode

    @cached_property
    def all_commits(self):
        commits = self.request(
                'repos',
                self.user,
                self.repo,
                'commits'
        )
        debug('Collecting %s commits', len(commits))
        return [self.request('repos',
                             self.user,
                             self.repo,
                             'commits',
                             commit['sha']) for commit in commits]

    def fetch_post_info(self, filename):
        for commit in reversed(self.all_commits):
            for post in commit['files']:
                if post['filename'] == filename:
                    author = commit['commit']['author']['name']
                    date = commit['commit']['author']['date']
                    debug('File %s was created on %s by %s', filename, date, author)
                    return author, date


def fetch_posts(**kwargs):
    bucket = PostAggregator(**kwargs)
    for sha, filename in bucket.collect_posts():
        content = bucket.fetch_post_content(sha, filename)
        author, date = bucket.fetch_post_info(filename)
        yield filename, author, date, content


if __name__ == '__main__':
    fetch_posts(repo='posts',
                exclude=(),
                user=None,
                password=None,
                branch='master')
