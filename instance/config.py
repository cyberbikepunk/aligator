""" This module contains sensitive configaration information. """

from os.path import join
from os.path import dirname


BASE_DIR = dirname(__file__)
POST_FILE = '/home/loic/Documents/posts/decorator_tutorial.ipynb'
MINI_CV = 'https://gist.githubusercontent.com/cyberbikepunk/29ff425054b71ea9220f/raw'
PITCH_URL = 'https://gist.githubusercontent.com/cyberbikepunk/29ff425054b71ea9220f/raw'
PROFILE_FILE = join('/home/loic/Code/charm/blog/instance/profile.yml')


SQLALCHEMY_DATABASE_URI = 'sqlite:////home/loic/Code/charm/blog/development.sqlite'
USER_PROFILE_FILE = '/home/loic/Code/charm/blog/instance/profile.yml'
DEBUG_AGGREGATOR = False
GITHUB_API_URL = 'api.github.com'

# The GitHub Repository where the blog content is stored
TOKEN = '128739f3efbb18f804e6c4cc8f29ea6c16d18754'
USER = 'cyberbikepunk'
BRANCH = 'master'
REPO = 'posts'
EXCLUDE = ['README.md', 'LICENSE.md']
