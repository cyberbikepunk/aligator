""" This module defines the data models for the blog blueprint. Heads up: there is no database. """


from arrow import get
from os.path import splitext
from json import loads
from slugify import slugify
from werkzeug.utils import cached_property
from instance.settings import JUMBO, STICKY
from ..utilities.aggregator import fetch_posts


class Post(object):
    def __init__(self,
                 filename,
                 author,
                 commit_date,
                 commit_message,
                 content):

        self.filename = filename
        self.slug = slugify(self.file_stem)
        self.author = author
        self.last_commit_message = commit_message
        self.last_commit_date = get(commit_date).datetime
        self.content = content

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
    def is_notebook(self):
        return self.file_extension is 'ipynb'

    @property
    def is_markdown(self):
        return self.file_extension is 'md'

    @cached_property
    def json(self):
        if self.is_notebook:
            return loads(self.content)

    def trim_line(self, line_nb):
        if self.is_notebook:
            line = self.json.cells[0]['source'][line_nb]
        else:
            line = self.content[line_nb]
        return line.rstrip(r'\n').rstrip().lstrip('#').lstrip()

    @cached_property
    def title(self):
        return self.trim_line(0)

    @cached_property
    def excerpt(self):
        return self.trim_line(2)


posts = []
for post in fetch_posts():
    posts.append(Post(*post))
    print(Post(*post))

if __name__ == '__main__':
    pass
