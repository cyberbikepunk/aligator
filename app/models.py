""" This module define the database model. """


from arrow import get
from os.path import splitext
from json import loads
from manage import db
from slugify import slugify
from werkzeug.utils import cached_property
from instance.settings import JUMBO, STICKY


VALID_EXTENSIONS = ('ipynb', 'md')


class FileFormatException(Exception):
    pass


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slug = db.Column(db.String, unique=True)
    filename = db.Column(db.String)
    author = db.Column(db.Unicode)
    last_commit_date = db.Column(db.DateTime)
    last_commit_message = db.Column(db.Unicode)
    content = db.Column(db.UnicodeText)
    test = db.Column(db.String)
    another_column = db.Column(db.Integer)

    def __init__(self,
                 filename,
                 author,
                 commit_date,
                 commit_message,
                 content):

        if self.file_extension not in VALID_EXTENSIONS:
            raise FileFormatException('Valid file extensions are %s' % str(VALID_EXTENSIONS))

        self.slug = slugify(self.file_stem)
        self.filename = filename
        self.author = author
        self.last_commit_message = commit_message
        self.last_commit_date = get(commit_date).datetime
        self.content = content

    def __repr__(self):
        return '<Post: %s>' % self.title

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


if __name__ == '__main__':
    pass
