""" Error handlers for the blog blueprint. """


from flask import render_template
from app.blog import blog


@blog.app_errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@blog.app_errorhandler(500)
def internal_server_error():
    return render_template('500.html'), 500
