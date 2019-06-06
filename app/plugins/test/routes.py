from app.plugins.test import plugin

@plugin.route('/')
def test():
    return '<h1>This is your example plugin route</h1>'

@plugin.route('/restricted')
@plugin.required_roles('test1')
def restricted():
    return '<h1>This is your example of a restricted route</h1>'