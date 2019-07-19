from app.plugins.test import plugin
from flask_login import current_user
from flask import abort

@plugin.before_request
def validate_logged_in():
    pass
    # remove the comments below to restrict entire blueprint to only authenticated users.
    # if not current_user.is_authenticated:
    #     abort(401)

@plugin.route('/')
def test():
    return '<h1>This is your example plugin route</h1>'

@plugin.route('/restricted')
@plugin.required_roles('test1')
def restricted():
    return '<h1>This is your example of a restricted route</h1>'