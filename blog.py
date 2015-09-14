from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, Form
from wtforms.validators import DataRequired
from flask import Markup
from markdown import markdown
from os.path import dirname, join
from requests import get
from json import loads


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/loic/Code/charm/blog/blog.sqlite'

app.debug = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


BASE_DIR = dirname(__file__)
POSTS_DIR = join(BASE_DIR, 'posts')
MINI_CV = 'https://gist.githubusercontent.com/cyberbikepunk/29ff425054b71ea9220f/raw'
PITCH_URL = 'https://gist.githubusercontent.com/cyberbikepunk/29ff425054b71ea9220f/raw'


class NameForm(Form):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


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
    with open('/home/loic/Code/charm/blog/posts/decorator_experiments.ipynb') as f:
        nb = f.read()
        json = loads(nb)
    return render_template('notebook.html', notebook=json)


@app.route('/', methods=['GET', 'POST'])
def index():
    pitch = get(PITCH_URL)
    mini_cv = get(MINI_CV)
    return render_template('home.html', pitch=pitch.text, mini_cv=mini_cv.text)


@app.route('/blog/')
def blog():
    with open(join(POSTS_DIR, 'blog.md')) as f:
        archive = f.read()
    return render_template('blog.html', archive=archive)


if __name__ == '__main__':
    manager.run()
