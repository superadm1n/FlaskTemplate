from app.plugins.test import blueprint
from app.lib.route_access import required_roles


@blueprint.route('/')
def test():
    return '<h1>This is your example plugin route</h1>'

@blueprint.route('/restricted')
@blueprint.required_roles('test1')
def restricted():
    pass