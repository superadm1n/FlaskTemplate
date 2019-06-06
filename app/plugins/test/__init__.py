from app.plugins.Plugin import Plugin

blueprint = Plugin(
    'test_blueprint',
    __name__,
    url_prefix='/test',
    template_folder='templates',
    static_folder='static',
    required_roles=[]
)