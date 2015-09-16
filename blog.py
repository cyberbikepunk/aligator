from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Markup
from markdown import markdown
from os.path import dirname
from json import loads
from yaml import safe_load
from os.path import join


from app import app, manager, bootstrap, moment, db


BASE_DIR = dirname(__file__)
POST_FILE = '/home/loic/Documents/posts/decorator_tutorial.ipynb'
MINI_CV = 'https://gist.githubusercontent.com/cyberbikepunk/29ff425054b71ea9220f/raw'
PITCH_URL = 'https://gist.githubusercontent.com/cyberbikepunk/29ff425054b71ea9220f/raw'
PROFILE_FILE = join(BASE_DIR, 'instance', 'profile.yml')


@app.template_filter('markdown')
def markdown_filter(data):
    return Markup(markdown(data))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/nb')
def notebook():
    with open(PROFILE_FILE) as f:
        profile = safe_load(f)

    with open('/home/loic/Documents/posts/decorator_tutorial.ipynb') as f:
        nb = f.read()
        json = loads(nb)

    return render_template('notebook.html', notebook=json, profile=profile)


@app.route('/')
def index():
    """
    Render posts for the front page in t,
    and the blogger profile inside the sidebar.
    """

    with open(PROFILE_FILE) as f:
        profile = safe_load(f)

    jumbotron = 'I am the jumbotron'
    sticky = ['I am the first sticky post', 'I am the second sticky post']

    return render_template('home.html', profile=profile, jumbotron=jumbotron, sticky=sticky)


@app.route('/blog/')
def blog():

    with open(PROFILE_FILE) as f:
        profile = safe_load(f)

    jumbotron = 'I am the jumbotron'
    sticky = ['I am the first sticky post', 'I am the second sticky post']

    with open(POST_FILE) as f:
        archive = f.read()
    return render_template('archive.html', archive=archive, profile=profile, jumbotron=jumbotron, sticky=sticky)


if __name__ == '__main__':
    manager.run()
