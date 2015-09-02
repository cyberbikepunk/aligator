from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<user>/')
def user(user):
    return 'Hello %s!' % user


if __name__ == '__main__':
    app.run()
