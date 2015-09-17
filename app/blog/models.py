""" This module define the database model. """

from instance.config import USER_PROFILE_FILE
from os.path import splitext
from yaml import load
from manage import db

with open(USER_PROFILE_FILE) as f:
    sticky_posts = load('sticky')
    jumbotron = load('jumbotron')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_commit_date = db.Column(db.DateTime)
    last_commit_date = db.Column(db.DateTime)
    content = db.Column(db.UnicodeText)
    filename = db.Column(db.String, unique=True)

    def __init__(self, filename, commit_date, content):
        self.filename = filename
        self.last_commit_date = commit_date
        self.first_commit_date = None
        self.content = content

    def __repr__(self):
        return '<Post %s: %s>' % (self.id, self.name)

    @property
    def is_sticky(self):
        return self.filename.isupper()

    @property
    def name(self):
        return splitext(self.filename)[0]

    @property
    def extension(self):
        return splitext(self.filename)[1]


if __name__ == '__main__':
    print(sticky_posts)
    print(jumbotron)
