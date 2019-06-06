from flask import Blueprint, abort
from flask_login import current_user
from functools import wraps

class Plugin(Blueprint):
    '''
    This class represents a plugin object, It should be used when extending the system via plugins
    '''
    def __init__(self, access_roles, *args, **kwargs):
        '''

        :param required_roles: The roles that will be used when restricting access to routes contained in the plugin
        :param args: Arguments that are passed to the flask.Blueprint object
        :param kwargs: Keyword arguments that are passed to the flask.Blueprint object
        '''
        super().__init__(*args, **kwargs)
        self.access_roles = access_roles

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
