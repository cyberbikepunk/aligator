from flask import render_template
from json import loads
from markdown import markdown
from yaml import safe_load
from instance.config import PROFILE_FILE, POST_FILE
from flask import Markup
from . import main


@main.app_template_filter('markdown')
def markdown_filter(data):
    return Markup(markdown(data))


@main.route('/nb')
def notebook():
    with open(PROFILE_FILE) as f:
        profile = safe_load(f)

    with open('/home/loic/Documents/posts/decorator_tutorial.ipynb') as f:
        nb = f.read()
        json = loads(nb)

    return render_template('notebook.html', notebook=json, profile=profile)


@main.route('/')
def home():
    """ Show a main column and a sidebar. """

    with open(PROFILE_FILE) as f:
        profile = safe_load(f)

    jumbotron = 'I am the jumbotron'
    sticky = ['I am the first sticky post', 'I am the second sticky post']

    return render_template('home.html', profile=profile, jumbotron=jumbotron, sticky=sticky)


@main.route('/posts/')
def posts():
    """ Show the post archive """

    with open(PROFILE_FILE) as f:
        profile = safe_load(f)

    jumbotron = 'I am the jumbotron'
    sticky = ['I am the first sticky post', 'I am the second sticky post']

    with open(POST_FILE) as f:
        archive = f.read()
    return render_template('archive.html', archive=archive, profile=profile, jumbotron=jumbotron, sticky=sticky)
