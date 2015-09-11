""" This module aggregates content from other websites. """


from os.path import dirname, join
from requests import get
from json import loads
from yaml import safe_load
from pprint import pprint


YAML_FILEPATH = join(dirname(__file__), 'aggregator.yml')
TEMP_DIR = join(dirname(__file__), 'temp')


class Aggregator(object):
    parameters = None

    def __init__(self):
        with open(YAML_FILEPATH) as f:
            self.parameters = safe_load(f)


class PostAggregator(Aggregator):
    token = str()
    user = str()
    branch = str()
    exclude = list()
    repo = str()

    def __init__(self):
        super(PostAggregator, self).__init__()
        self.__dict__.update(self.parameters['github'])
        self.query = {'token': self.token}
        self.api_url = 'https://api.github.com/'
        self.raw_url = 'https://raw.githubusercontent.com/'

    def get_posts_repo(self):
        self.request_json(self.api_url + 'repos/' + self.user + '/' + self.repo)

    def request_json(self, url):
        response = get(url=url, params=self.query)
        if response.status_code == 200:
            json = loads(response.text)
            pprint(json)
            return json
        else:
            print(response.url)
            print(response.status_code)

    def get_posts_master_branch_hash(self):
        json = self.request_json(self.api_url + 'repos/' + self.user + '/' + self.repo + '/branches/' + self.branch)
        sha = json['commit']['sha']
        return sha

    def get_archive_link(self):
        self.request_tarball(self.api_url + 'repos/' + self.user + '/' + self.repo + '/tarball/' + self.branch)

    def request_tarball(self, url):
        response = get(url=url, params=self.query)
        if response.status_code == 200:
            json = open(response.text)
            pprint(json)
            return json

    def request_file(self, file):
        self.download(self.raw_url + self.user + '/' + self.repo + '/' + self.branch + '/' + file)

    @staticmethod
    def download(url):
        response = get(url)
        if response.status_code == 200:
            return response.text

    def get_tree(self, sha):
        self.request_json(self.api_url + 'repos/' + self.user + '/' + self.repo + '/git/trees/' + sha)

if __name__ == '__main__':
    a = PostAggregator()
    sha = a.get_posts_master_branch_hash()
    a.get_tree(sha)
    a.request_file('README.md')
