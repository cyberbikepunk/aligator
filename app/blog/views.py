""" The blog blueprint (prefix: /blog) has two views: single and multiple posts. """


from flask import render_template, abort
from markdown import markdown
from flask import Markup
from importlib import reload

from app.blog import blog
from instance.profile import PROFILE as USER
from app.blog.models import archive


@blog.app_template_filter('markdown')
def markdown_filter(data):
    return Markup(markdown(data))


@blog.route('/')
def multiple_posts():
    return render_template('archive.html', profile=USER, archive=archive)


@blog.route('/reload')
def reload_posts():
    reload('app.models')


@blog.route('/<slug>')
def single_post(slug):
    post = archive.from_slug(slug)

    if not post:
        return abort(404)

    return render_template(post.template, post=post, profile=USER, archive=archive)
