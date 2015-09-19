""" This module holds the model for the blog blueprint. Heads up: there is no database. """


from arrow import get
from os.path import splitext
from json import loads
from slugify import slugify
from werkzeug.utils import cached_property
from instance.settings import JUMBO, STICKY
from ..utilities.aggregator import fetch_posts
from instance.settings import GITHUB_REPO, GITHUB_EXCLUDE, GITHUB_TOKEN, GITHUB_USER, GITHUB_BRANCH


class Post(object):
    def __init__(self,
                 filename,
                 author,
                 commit_date,
                 commit_message,
                 content):

        self.filename = filename
        self.author = author
        self.last_commit_message = commit_message
        self.last_commit_date = get(commit_date)
        self.content = content
        self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post: %s>' % self.title

    def __str__(self):
        return self.title

    @property
    def file_stem(self):
        return splitext(self.filename)[0]

    @property
    def file_extension(self):
        return splitext(self.filename)[1]

    @property
    def is_jumbo(self):
        return self.filename in JUMBO

    @property
    def is_sticky(self):
        return self.filename in STICKY

    @property
    def is_normal(self):
        return not self.is_jumbo and not self.is_sticky

    @property
    def is_notebook(self):
        return self.file_extension == '.ipynb'

    @property
    def is_markdown(self):
        return self.file_extension == '.md'

    @cached_property
    def json(self):
        if self.is_notebook:
            return loads(self.content)

    @property
    def top_lines(self):
        if self.is_notebook:
            return [line.rstrip() for line in self.json['cells'][0]['source']]
        else:
            return self.content.split('\n')

    @cached_property
    def title(self):
        return self.top_lines[0].lstrip('#').lstrip()

    @cached_property
    def excerpt(self):
        return self.top_lines[2]

    @cached_property
    def timestamp(self):
        return self.last_commit_date.format('dddd D MMMM YYYY')


# There's no database: posts are imported from GitHub
posts = [Post(*post) for post in fetch_posts(GITHUB_REPO,
                                             GITHUB_EXCLUDE,
                                             GITHUB_TOKEN,
                                             GITHUB_USER,
                                             GITHUB_BRANCH)]
