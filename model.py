""" This module define the database model. """


from datetime import datetime
from blog import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    website = db.Column(db.String, db.ForeignKey('source.website'), nullable=False)
    title = db.Column(db.UnicodeText, nullable=False)
    token = db.Column(db.String, nullable=False)
    excerpt = db.Column(db.UnicodeText)
    body = db.Column(db.UnicodeText)
    publication_date = db.Column(db.DateTime)
    url = db.Column(db.String)
    filename = db.Column(db.String)

    source = db.relationship('Source', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, website, token):
        self.title = title
        self.website = website
        self.token = token
        self.created = datetime.now()

    def __repr__(self):
        return '<Post=%s>' % self.title

    @property
    def is_sticky(self):
        return self.filename.isupper()

    @property
    def priority(self):
        return 1


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    website = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, website, username, password, url):
        self.website = website
        self.password = password
        self.username = username
        self.url = url

    def __repr__(self):
        return '<Source=%s>' % self.website


if __name__ == '__main__':
    db.create_all()
