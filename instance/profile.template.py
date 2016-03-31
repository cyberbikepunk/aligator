""" User defined settings. Rename this file to profile.py to make it work!  """


# Change settings here
# ====================

BLOG = "my blog"
GREETING = "my great greeting phrase"
BASELINE = "my great baseline"

REPO = 'https://github.com/username/repo'
RESUME_URL = 'https://jsonresume.org/username'

PHOTO = 'photo.jpg'
FAVICON = 'favicon.ico'
LOGO = 'logo.png'

NAME = 'Mickey Mouse'
TITLE = 'Actor'
EMAIL = 'your@email.com'
LOCATIONS = ['Hollywood']

PITCH = '''
    I'm a regular person.
    I'm a bizarre person.
'''

TAGS = [
    'python',
    'php',
    'ruby',
    'etc'
]

ACCOUNTS = [
    {'name': 'twitter', 'link': 'https://twitter.com/your_account'},
    {'name': 'stackoverflow', 'link': 'http://stackoverflow.com/users/XXXXXXX/your_account'},
    {'name': 'github', 'link': 'https://github.com/your_account'},
    {'name': 'linkedin', 'link': 'https://de.linkedin.com/in/your_account'},
]

ORGANISATIONS = [
    {'name': 'organisation 1', 'link': 'http://your_organisation.com'},
    {'name': 'organisation 2', 'link': 'http://another_organisation.com'},
]

GITHUB = {
    'token': 'your_github_token_here',
    'user': 'your_github_username',
    'branch': 'your_master_branch_most_probably',
    'repo': 'your_post_repo_name',
    'exclude': ['README.md', 'LICENSE.md']
}

JUMBO = ['post1.md']
STICKY = ['post2.md']


# Do not modify
# =============

PROFILE = {
    'blog': BLOG,
    'greeting': GREETING,
    'baseline': BASELINE,
    'photo': PHOTO,
    'logo': LOGO,
    'favicon': FAVICON,
    'name': NAME,
    'title': TITLE,
    'email': EMAIL,
    'locations': LOCATIONS,
    'tags': TAGS,
    'accounts': ACCOUNTS,
    'organisations': ORGANISATIONS,
    'pitch': PITCH,
    'jumbo': JUMBO,
    'sticky': STICKY,
    'github': GITHUB
}
