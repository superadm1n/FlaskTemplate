from flask import Blueprint


class Plugin(Blueprint):
    '''
    This class represents a plugin object, It should be used when extending the system via plugins
    '''
    def __init__(self, required_roles, *args, **kwargs):
        '''

        :param required_roles: The roles that will be used when restricting access to routes contained in the plugin
        :param args: Arguments that are passed to the flask.Blueprint object
        :param kwargs: Keyword arguments that are passed to the flask.Blueprint object
        '''
        super().__init__(*args, **kwargs)
        self.required_roles = required_roles