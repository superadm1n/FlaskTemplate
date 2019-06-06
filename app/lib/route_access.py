from flask import redirect, url_for, abort
from flask_login import current_user
from functools import wraps


def required_roles(*roles):
    '''Custom function for checking if a user has the required rolls to access a resource.
    :param roles:
    :return:
    '''

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                if current_user.has_role(*roles) is False:
                    abort(401)
            except AttributeError:
                abort(401)
            return f(*args, **kwargs)

        return wrapped
    return wrapper
