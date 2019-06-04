from app.plugins.test import blueprint


@blueprint.route('/')
def test():
    return '<h1>This is your example plugin route</h1>'