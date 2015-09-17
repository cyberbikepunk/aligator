""" The blueprint for the blog. """

from flask import Blueprint
main = Blueprint('main', __name__)
from . import views
