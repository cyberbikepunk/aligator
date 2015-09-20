""" This module holds the model for the blog blueprint.

Heads up: there is no database. Posts are imported from GitHub when the application
starts up and stored in memory. The Archive class simulates the database query interface.

"""
from itertools import chain

from arrow import get
from os.path import splitext
from json import loads
from slugify import slugify
from werkzeug.utils import cached_property
from instance.settings import JUMBO, STICKY
from ..utilities.aggregator import fetch_posts
from instance.settings import GITHUB


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
        return self.top_lines[0].lstrip('#').lstrip().rstrip('#')

    @cached_property
    def excerpt(self):
        return self.top_lines[2]

    @cached_property
    def timestamp(self):
        return self.last_commit_date.format('dddd D MMMM YYYY')

    @property
    def template(self):
        return 'notebook.html' if self.is_notebook else 'markdown.html'

    @cached_property
    def body(self):
        """ Return the markdown content excluding the title and the excerpt. """
        if self.is_notebook:
            new = self.json
            new['cells'][0]['source'] = new['cells'][0]['source'][4:]
            return new
        else:
            return '\n'.join(self.top_lines[4:])

    @staticmethod
    def is_header(line):
        return line.startswith('#')


class Archive(object):
    def __init__(self, posts_):
        self.posts = posts_

    def __repr__(self):
        return '<Archive: %s posts>' % len(self.posts)

    def from_slug(self, slug):
        for p in self.posts:
            if p.slug == slug:
                return p

    def from_author(self, author):
        for p in self.posts:
            if p.slug == author:
                return p

    @property
    def sticky_posts(self):
        return [p for p in self.posts if p.is_sticky]

    @property
    def jumbo_posts(self):
        return [p for p in self.posts if p.is_jumbo]

    @property
    def normal_posts(self):
        return [p for p in self.posts if p.is_normal]

    @property
    def by_importance(self):
        return list(chain(self.jumbo_posts, self.sticky_posts, self.normal_posts))


posts = [Post(*post) for post in fetch_posts(**GITHUB)]
archive = Archive(posts)
