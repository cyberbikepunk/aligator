""" User defined settings. Rename this file to settings.py to make it work! """


# Change your settings here
# =========================

_BLOG = 'cyberbikepunk'
_GREETING = "Mostly about python ! A tech blog brought to you by cyberbikepunk."
_BASELINE = "cyberbikepunk's blog - Mostly about python !"

_REPO = 'https://github.com/cyberbikepunk/posts'

_PHOTO = 'photo2.jpg'
_FAVICON = 'favicon.ico'
_LOGO = 'logo.png'

_NAME = 'Loic Jounot'
_TITLE = 'Python developper'
_EMAIL = 'loic@cyberpunk.bike'
_LOCATIONS = ['Berlin']

_PITCH = '''
    I love all things python.
    I like linux most of the time. Sometimes I hate git.
    I eat data for breakfast.
    I would open-source the world if I could.
    I don't do front-end, even under torture.
'''

_TAGS = [
    'python',
    'pandas',
    'matplotlib',
    'bokeh',
    'seaborn',
    'numpy',
    'scipy',
    'sqlalchemy',
    'scrapy',
    'bootstrap',
    'pythonanywhere',
    'dataviz',
    'maths',
    'stats',
    'open-source',
    'creative-commons',
    'decentralize',
]

_ACCOUNTS = [
    {'name': 'twitter', 'link': 'https://twitter.com/your_account'},
    {'name': 'stackoverflow', 'link': 'http://stackoverflow.com/users/XXXXXXX/your_account'},
    {'name': 'github', 'link': 'https://github.com/your_account'},
    {'name': 'linkedin', 'link': 'https://de.linkedin.com/in/your_account'},
]

_ORGANISATIONS = [
    {'name': 'coding amigos', 'link': 'http://your_organisation.com'},
    {'name': 'cogeeks', 'link': 'http://another_organisation.com'},
]

GITHUB = {
    'token': 'your_github_token_here',
    'user': 'your_github_username',
    'branch': 'yout_master_branch_most_proabably',
    'repo': 'your_post_repo_name',
    'exclude': ['README.md', 'LICENSE.md']
}

JUMBO = ['hello.md']
STICKY = ['micro_cv.md']


# The agglomerated user-profile: do not modify
# ============================================

USER_PROFILE = {
    'blog': _BLOG,
    'greeting': _GREETING,
    'baseline': _BASELINE,
    'photo': _PHOTO,
    'logo': _LOGO,
    'favicon': _FAVICON,
    'name': _NAME,
    'title': _TITLE,
    'email': _EMAIL,
    'locations': _LOCATIONS,
    'tags': _TAGS,
    'accounts': _ACCOUNTS,
    'organisations': _ORGANISATIONS,
    'pitch': _PITCH,
}
