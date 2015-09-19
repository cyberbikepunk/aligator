""" This module holds three views: home, post and about. """

from json import loads

from flask import render_template
from markdown import markdown
from flask import Markup

from . import blog
from instance.settings import USER_PROFILE
from .models import posts


@blog.app_template_filter('markdown')
def markdown_filter(data):
    return Markup(markdown(data))


@blog.route('/notebook-test')
def notebook():

    with open('/home/loic/Documents/posts/decorator_tutorial.ipynb') as ipynb:
        nb = ipynb.read()
        json = loads(nb)

    return render_template('notebook.html', notebook=json, profile=USER_PROFILE)


@blog.route('/')
def home():

    jumbotron = 'I am the jumbotron'
    sticky = ['I am the first sticky post', 'I am the second sticky post']

    return render_template('home.html', profile=USER_PROFILE, jumbotron=jumbotron, sticky=sticky)


@blog.route('/archive')
def archive():
    return render_template('archive.html', posts=posts, profile=USER_PROFILE)
