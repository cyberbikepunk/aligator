from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from wtforms import StringField, SubmitField, Form
from wtforms.validators import DataRequired
from flask import Markup
from markdown import markdown
from os.path import realpath, dirname, join

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


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


@app.route('/', methods=['GET', 'POST'])
def index():
    cwd = dirname(realpath(__file__))
    with open(join(cwd, 'posts/test.md')) as f:
        post = f.read()
    return render_template('index.html', post=post)


if __name__ == '__main__':
    manager.run()
