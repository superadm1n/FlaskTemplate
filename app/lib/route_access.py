from flask import redirect, url_for
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
                if bool(set(roles) & {role.name for role in current_user.roles}) is False:
                    return redirect(url_for('base_blueprint.route_default'))
            except AttributeError:
                return redirect(url_for('base_blueprint.route_default'))
            return f(*args, **kwargs)

        return wrapped
