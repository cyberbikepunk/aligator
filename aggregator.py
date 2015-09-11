""" This module aggregates content from other websites. """


from os.path import dirname, join
from requests import get
from json import loads
from yaml import safe_load
from base64 import b64decode
from blog import app
from murls import https

YAML_FILEPATH = join(dirname(__file__), 'aggregator.yml')
TEMP_DIR = join(dirname(__file__), 'temp')


class Aggregator(object):
    parameters = None

    def __init__(self):
        with open(YAML_FILEPATH) as f:
            self.parameters = safe_load(f)


class PostAggregator(Aggregator):
    url = https('api.github.com')

    token = ''
    user = ''
    branch = ''
    repo = ''
    exclude = []

    def __init__(self):
        super(PostAggregator, self).__init__()
        self.__dict__.update(self.parameters['github'])

    def request_json(self, url):
        response = get(url=url, params={'token': self.token})

        if response.status_code == 200:
            json = loads(response.text)
            return json
        else:
            app.logger.error('%s failed with %s ',
                             response.url, response.status_code)

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

    pa = PostAggregator()
    repo = pa.get_repo_hash()
    files = pa.get_file_hashes(repo)

    for file_id in files:
        text = pa.get_file_content(file_id)
        print(text)
