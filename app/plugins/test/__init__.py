from app.plugins.Plugin import Plugin

blueprint = Plugin(
    name='test_blueprint',
    import_name=__name__,
    url_prefix='/test',
    template_folder='templates',
    static_folder='static',
    access_roles=['test1', 'test2', 'test3']
)