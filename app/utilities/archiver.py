""" This module snchronises the database with the post reposotory on GitHub. """


from model import db
from app.utilities.aggregator import aggregate


def synchronize():

    posts = aggregate()

    db.session
