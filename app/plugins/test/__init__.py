from app.plugins.Plugin import Plugin

plugin = Plugin(
    name='test_plugin',
    import_name=__name__,
    url_prefix='/test',
    template_folder='templates',
    static_folder='static',
    access_roles=['test1', 'test2', 'test3']
)